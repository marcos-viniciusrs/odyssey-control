# Odyssey Control

Painel local em http://IP_DO_NOTEBOOK:8766. O endereço é detectado na inicialização e pode mudar com DHCP. Qualquer dispositivo na sub-rede autorizada pode operar o monitor. Evite redes não confiáveis. Não há autenticação ou TLS.

Brilho, contraste e RGB estão disponíveis. Somente o brilho foi verificado com escrita. Perfis são armazenados no navegador do celular. Entrada e energia são exibidas em leitura, sem comandos de troca ou desligamento. O painel permanece acessível se o monitor desaparecer. Atualize manualmente para tentar nova leitura.

O serviço inicia no boot via systemd de usuário e linger. O usuário local foi incluído no grupo i2c para acesso persistente aos dispositivos I²C. A regra padrão do sistema atribui esses dispositivos ao grupo i2c. A nova associação de grupo entra em vigor em novos processos de login e após reiniciar o computador. A sessão atual continua com acesso via uaccess. Consulte INSTALL.md.

A seção Recursos experimentais consulta sob demanda os códigos candidatos de modo de imagem, Black Equalizer e Adaptive-Sync. Os nomes ainda não foram validados no G55C LS32CG552ELMZD e os valores são apresentados em leitura apenas.
