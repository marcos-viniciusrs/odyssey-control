# API

GET /api/status, /api/monitor, /api/settings, /api/vcp e /api/capabilities. POST /api/brightness, /api/contrast, /api/red, /api/green e /api/blue aceitam JSON {"value": inteiro}. As escritas exigem Origin igual ao endereço do serviço e Content-Type application/json. O limite é obtido do monitor antes da escrita. Não há endpoint de escrita arbitrária nem para entrada e energia. Perfis pertencem ao armazenamento local do navegador.
