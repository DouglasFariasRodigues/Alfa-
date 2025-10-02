# language: pt
Funcionalidade: Gerenciar ofertas e distribuição para ONGs

  Cenário: Admin gerencia valores de oferta direcionados para ONG
    Dado que existe um Admin logado
    E existe uma ONG "Cruz Vermelha" cadastrada
    E existe uma oferta de valor 1000.00
    Quando o Admin direciona 500.00 da oferta para "Cruz Vermelha" via "Transferência bancária"
    Então a distribuição deve ser registrada com sucesso
    E a oferta deve ter uma distribuição de 500.00 para "Cruz Vermelha"

  Cenário: Admin direciona oferta para múltiplas ONGs
    Dado que existe um Admin logado
    E existe uma ONG "Cruz Vermelha" cadastrada
    E existe uma ONG "Médicos Sem Fronteiras" cadastrada
    E existe uma oferta de valor 2000.00
    Quando o Admin direciona 800.00 da oferta para "Cruz Vermelha" via "PIX"
    E o Admin direciona 700.00 da oferta para "Médicos Sem Fronteiras" via "Transferência bancária"
    Então a oferta deve ter 2 distribuições registradas
    E o total distribuído deve ser 1500.00

  Cenário: Admin visualiza todas as distribuições de ofertas
    Dado que existe um Admin logado
    E existe uma ONG "Cruz Vermelha" cadastrada
    E existe uma oferta de valor 1000.00 com distribuição para "Cruz Vermelha"
    Quando o Admin solicita visualizar todas as distribuições
    Então o Admin deve ver pelo menos 1 distribuição
