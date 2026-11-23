# Monitor e pesquisa VCP

EDID SAM produto 0x7489, nome Odyssey G5, semana 14 de 2025. Controlador MStar, firmware comunicado 0.1. Modelo comercial informado pelo proprietário: LS32CG552ELMZD. Software informado pelo menu: M-C5500GGZA-1008.3. A versão 0.1 acima é a resposta de identificação DDC, não a versão do software exibida no menu. Conector card1-DP-1, I²C 12 na medição. capabilities falhou com máximo de tentativas.

| Código | Função | Resultado | Escrita |
|---|---|---|---|
| 10 | Brilho | 50/50 | Confirmada 50→49→50, inclusive pela API |
| 12 | Contraste | 50/50 | Não testada |
| 14 | Temperatura predefinida | 02 | Não testada |
| 16,18,1A | RGB | 50/100 cada | Não testada |
| 60 | Entrada | 0f DisplayPort | DP e HDMI-1 foram confirmados em sessão anterior, sem troca neste teste |
| 87 | Nitidez | 0a | Não testada |
| D6 | Energia | 00 | Não testada, interpretação incerta |
| 0B | Incremento temperatura | ERR | Não testada |
| 0C | Solicitação temperatura | 0/2 | Não testada |
| 62 | Volume | 5/100 | Não testada |
| 72,86,AC,AE | Controles adicionais | ERR | Não testada |
| B6 | Tecnologia painel | 03 | Não testada |
| C8,C9,DF,DC | Identificação e modo | Responderam | Não testada |

ERR é falha de leitura, não comprova ausência. Gamma, equalizador, FreeSync, HDR, latência e modos proprietários não foram confirmados. Não há escrita proprietária habilitada. Comandos E0–FF são reservados ao fabricante e não foram investigados por varredura. O KScreen reporta DP-1 em 2560×1440 a 164,83 Hz e escala 1. Configurações KScreen dependem da sessão e não são DDC. Energia e recuperação em standby não foram testadas.

Fontes: https://www.ddcutil.com/command_getvcp/ ; https://www.ddcutil.com/command_capabilities/ ; https://www.ddcutil.com/sniffing/ ; https://www.ddcutil.com/i2c_permissions/ ; https://www.ddcutil.com/mccs_background/

## Pesquisa adicional de 23/11/2026

Leituras direcionadas por ddcutil getvcp, sem escrita, no monitor identificado acima.

| Código | Resposta bruta | Significado proposto em outro modelo | Situação neste G5 |
|---|---|---|---|
| 2D | máximo 0x000a, atual 0x0008 | modo de imagem | Leitura respondeu; significado não confirmado |
| 2F | máximo 0x000a, atual 0x0005 | Black Equalizer | Leitura respondeu; significado não confirmado |
| F2 | máximo 0x0001, atual 0x0000 | Adaptive-Sync | Leitura respondeu; significado não confirmado |
| 0A | ddcutil recusou leitura, identifica como restauração de fábrica | Eye Saver em G60SD no protocolo proprietário | Não executado; conflito de interpretação |

Os significados propostos vêm do protocolo odyssey-ctl, testado no Odyssey OLED G6 G60SD. O mesmo código pode ter outra função em outro modelo. Não houve comparação com o menu físico ou teste de escrita. O perfil estendido usa escritas em EB e não foi acionado.

O odyssey-ctl oferece CLI de leitura e documentação de funções e perfis. Sua compatibilidade com outros Odyssey não foi confirmada pelo autor. O ddcutil permite consultas individuais e sua documentação explica que a lista de capacidades pode falhar ou ser incompleta. Não houve varredura indiscriminada.

Pesquisas de firmware G55C descrevem outro modelo específico, incluindo operações que podem alterar configurações persistentes. O projeto monitor-firmware cita suporte G5 planejado. A documentação do ddcutil descreve captura do tráfego DDC e a dificuldade adicional pelo DisplayPort. Nenhum firmware ou ferramenta de terceiros foi instalado.

Há relatos de falhas de brilho em um G5 S27DG50 e um problema do KDE PowerDevil registrado como corrigido no Plasma 6.4.1. Um relato no fórum Samsung Odyssey menciona correção por firmware em um G50D. Não se sabe se os relatos afetam o monitor detectado. A Samsung orienta identificar o código comercial exato antes de obter firmware correspondente.

Fontes:

- https://github.com/deddroid/odyssey-ctl/blob/main/docs/PROTOCOL.md
- https://github.com/deddroid/odyssey-ctl
- https://www.ddcutil.com/command_capabilities/
- https://www.ddcutil.com/sniffing/
- https://github.com/c8dhjp4tyv-bit/odyssey-g5-firmware-research
- https://github.com/franc1sc0sv/monitor-firmware
- https://github.com/rockowitz/ddcutil/issues/466
- https://bugs.kde.org/show_bug.cgi?id=494522
- https://www.reddit.com/r/SamsungOdyssey/comments/1g9n6t1/samsung_odyssey_g5_brightness/
- https://www.samsung.com/us/support/troubleshoot/TSG10010570/

## Pesquisa específica do LS32CG552ELMZD

O proprietário informou o modelo LS32CG552ELMZD e o software M-C5500GGZA-1008.3. A Samsung identifica este produto como G55C de 32 polegadas, QHD, até 165 Hz, com uma entrada DisplayPort 1.2 e uma HDMI 2.0. A página oficial lista FreeSync, HDR10, Eye Saver, Black Equalizer, Low Input Lag e Virtual Aim Point. Isso confirma a existência dessas funções no produto, não sua controlabilidade por DDC. HDMI 2 não consta nas especificações.

Em 23/11/2026, a página de suporte brasileira do modelo exato apresentava arquivo USB versão 1008.3, igual à versão informada. A página também lista Samsung Display Manager para Windows e macOS. Não foi encontrado pacote Linux nessa listagem e não foi realizada atualização.

O projeto odyssey-g5-firmware-research estudou outro código regional, LS32CG552EUXUF. Os autores relatam que um arquivo 1010.0 fornecido por proprietário é uma derivação personalizada do arquivo 1008.3, com partições executáveis idênticas entre as duas amostras. Não há verificação de identidade entre essas amostras e o firmware instalado neste monitor, nem compatibilidade comprovada entre as variantes. O estudo reporta consequências arriscadas ao modificar menus de fábrica. Nenhum firmware modificado foi instalado.

As leituras repetidas em 23/11/2026 retornaram 2D atual 8 de 10, 2F atual 5 de 10 e F2 atual 0 de 1. Um projeto diferente atribui esses códigos a modo de imagem, Black Equalizer e Adaptive-Sync em um G60SD. O nome de modo 8 coincide com Original na lista PC da página da Samsung, mas essa coincidência não comprova o mapeamento. A comparação com os valores do menu físico continua necessária. Nenhuma escrita em 2D, 2F ou F2 foi feita.

Fontes do modelo exato: https://www.samsung.com/br/support/model/LS32CG552ELMZD/ e https://www.samsung.com/br/monitors/gaming/odyssey-g5-g55c-32-inch-165hz-curved-qhd-ls32cg552elmzd/
Pesquisa de variante semelhante: https://github.com/c8dhjp4tyv-bit/odyssey-g5-firmware-research/blob/main/docs/FIRMWARE_ARCHITECTURE.md
Projeto de códigos para G60SD: https://github.com/deddroid/odyssey-ctl/blob/main/docs/PROTOCOL.md
