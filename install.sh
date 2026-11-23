#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
[[ -f /etc/arch-release ]] || { echo 'Este instalador requer Arch Linux.'; exit 1; }
for dependency in python3 ddcutil ip systemctl; do
  command -v "$dependency" >/dev/null || { echo "Dependência ausente: $dependency"; exit 1; }
done
mkdir -p "$HOME/.config/systemd/user"
unit="$HOME/.config/systemd/user/odyssey-control.service"
cat > "$unit" <<EOF
[Unit]
Description=Odyssey G5 web control
After=network-online.target
StartLimitIntervalSec=0
[Service]
WorkingDirectory=$PWD
Environment=ODYSSEY_PORT=8766
ExecStart=/usr/bin/python3 $PWD/server.py
Restart=on-failure
RestartSec=10
NoNewPrivileges=true
UMask=0077
[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now odyssey-control.service
printf 'Serviço instalado. Porta: 8766\n'
