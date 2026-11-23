#!/usr/bin/env python3
import http.server, ipaddress, json, os, pathlib, re, socket, subprocess, threading, time
from urllib.parse import urlsplit

BASE = pathlib.Path(__file__).resolve().parent
def lan_config():
    route = json.loads(subprocess.run(['ip', '-j', 'route', 'get', '1.1.1.1'], capture_output=True, text=True, check=True, timeout=5).stdout)[0]
    host = route['prefsrc']
    addresses = json.loads(subprocess.run(['ip', '-j', '-4', 'addr', 'show', 'dev', route['dev']], capture_output=True, text=True, check=True, timeout=5).stdout)
    prefix = next(a['prefixlen'] for device in addresses for a in device['addr_info'] if a['local'] == host)
    return host, ipaddress.ip_network(f'{host}/{prefix}', strict=False)

DETECTED_HOST, DETECTED_NETWORK = lan_config()
HOST = os.environ.get('ODYSSEY_HOST', DETECTED_HOST)
PORT = int(os.environ.get('ODYSSEY_PORT', '8765'))
NETWORK = ipaddress.ip_network(os.environ.get('ODYSSEY_NETWORK', str(DETECTED_NETWORK)), strict=False)
LOCK = threading.Lock()
RATE_LOCK = threading.Lock()
RECENT = {}
CODES = {'brightness':'10', 'contrast':'12', 'red':'16', 'green':'18', 'blue':'1a', 'input':'60', 'power':'d6', 'temperature':'14', 'sharpness':'87'}
EXPERIMENTAL_CODES = {'picture_mode': '2d', 'black_equalizer': '2f', 'adaptive_sync': 'f2'}

def monitor():
    found = []
    for p in pathlib.Path('/sys/class/drm').glob('card*-*'):
        try:
            edid = (p/'edid').read_bytes()
            if (p/'status').read_text().strip() != 'connected' or len(edid) < 128 or edid[8:12] != bytes.fromhex('4c2d8974') or b'Odyssey G5' not in edid:
                continue
            bus = (p/'ddc').resolve().name
            if re.fullmatch(r'i2c-\d+', bus):
                found.append((p.name, bus[4:]))
        except OSError:
            continue
    if len(found) != 1:
        raise RuntimeError('Monitor Odyssey G5 não encontrado ou seleção ambígua')
    return found[0]

def ddc(args):
    with LOCK:
        connector, bus = monitor()
        p = subprocess.run(['ddcutil', '--bus', bus, *args], capture_output=True, text=True, timeout=8)
        if p.returncode:
            raise RuntimeError((p.stderr or p.stdout).strip() or 'Falha DDC')
        return p.stdout.strip()

def read_features(codes):
    raw = ddc(['getvcp', *codes.values(), '--brief'])
    result = {}
    reverse = {v.upper(): k for k,v in codes.items()}
    for line in raw.splitlines():
        fields = line.split()
        if len(fields) >= 4 and fields[1] in reverse:
            try:
                if fields[2] == 'CNC' and len(fields) >= 7:
                    maximum = (int(fields[3][1:], 16) << 8) | int(fields[4][1:], 16)
                    value = (int(fields[5][1:], 16) << 8) | int(fields[6][1:], 16)
                else:
                    value = int(fields[3][1:], 16) if fields[3].startswith('x') else int(fields[3])
                    maximum = int(fields[4]) if len(fields) > 4 else None
                result[reverse[fields[1]]] = {'value': value, 'max': maximum}
            except ValueError: pass
    return result

def settings():
    return read_features(CODES)

class Handler(http.server.BaseHTTPRequestHandler):
    def allowed(self):
        try:
            peer = ipaddress.ip_address(self.client_address[0])
            now = time.monotonic()
            with RATE_LOCK:
                for key, timestamps in list(RECENT.items()):
                    RECENT[key] = [t for t in timestamps if now - t < 60]
                    if not RECENT[key]: del RECENT[key]
                timestamps = RECENT.setdefault(str(peer), [])
                if len(timestamps) >= 120: return False
                timestamps.append(now)
            host = self.headers.get('Host','')
            origin = self.headers.get('Origin')
            return (peer in NETWORK or peer.is_loopback) and host in (f'{HOST}:{PORT}', f'localhost:{PORT}', f'127.0.0.1:{PORT}') and (not origin or origin == 'http://' + host)
        except ValueError: return False
    def send(self, status, content, typ='application/json'):
        if isinstance(content, dict): content = json.dumps(content, ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type', typ); self.send_header('Content-Length', str(len(content))); self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(content)
    def do_GET(self):
        if not self.allowed(): return self.send(403, {'error':'Acesso negado'})
        path = urlsplit(self.path).path
        try:
            if path == '/': return self.send(200, (BASE/'index.html').read_bytes(), 'text/html; charset=utf-8')
            if path in ('/api/status','/api/monitor'):
                connector, bus = monitor(); return self.send(200, {'model':'Samsung Odyssey G5', 'connector':connector, 'bus':bus})
            if path in ('/api/settings','/api/vcp'): return self.send(200, {'settings':settings()})
            if path == '/api/experimental': return self.send(200, {'settings': read_features(EXPERIMENTAL_CODES), 'read_only': True})
            if path == '/api/capabilities': return self.send(200, {'info':'Leituras detectadas. Capacidades do monitor indisponíveis.'})
            return self.send(404, {'error':'Não encontrado'})
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as e: return self.send(503, {'error':str(e)})
    def do_POST(self):
        if not self.allowed() or self.headers.get('Origin') != 'http://' + self.headers.get('Host','') or self.headers.get('Content-Type') != 'application/json': return self.send(403, {'error':'Acesso negado'})
        name = urlsplit(self.path).path.removeprefix('/api/')
        if name not in ('brightness','contrast','red','green','blue'): return self.send(404, {'error':'Controle indisponível'})
        try:
            length = int(self.headers.get('Content-Length','0'))
            if not 0 < length <= 128: raise ValueError('Requisição inválida')
            value = json.loads(self.rfile.read(length))['value']
            if type(value) is not int or not 0 <= value <= 100: raise ValueError('Valor inválido')
            current = settings().get(name)
            if not current or current['max'] is None or value > current['max']: raise ValueError('Valor fora do limite do monitor')
            ddc(['setvcp', CODES[name], str(value)])
            return self.send(200, {'ok':True})
        except (ValueError, KeyError, json.JSONDecodeError) as e: return self.send(400, {'error':str(e)})
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as e: return self.send(503, {'error':str(e)})
    def log_message(self, fmt, *args): pass

class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True

Server((HOST, PORT), Handler).serve_forever()
