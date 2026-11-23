#!/bin/bash
set -e
systemctl --user disable --now odyssey-control.service || true
rm -f "$HOME/.config/systemd/user/odyssey-control.service"
systemctl --user daemon-reload
printf 'Serviço removido. Arquivos e dados do projeto preservados.\n'
