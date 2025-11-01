# language: pt
Funcionalidade: Admin gerencia sistema

  Cenário: Admin faz login para gerenciar publicações
    Dado que existe um Admin cadastrado com email "admin@igreja.com"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin acessa a área de publicações
    Então o Admin deve ter acesso às publicações

  Cenário: Admin faz login para gerenciar ofertas
    Dado que existe um Admin cadastrado com email "admin@igreja.com"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin acessa a área de ofertas
    Então o Admin deve ter acesso às ofertas

  Cenário: Admin registra oferta de forma transparente
    Dado que existe um Admin logado
    Quando o Admin registra uma oferta de 2500.00 com descrição "Oferta do culto de domingo"
    Então a oferta deve ser registrada como pública
    E a oferta deve estar visível para os membros

  Cenário: Admin registra oferta e distribui para ONGs
    Dado que existe um Admin logado
    E existe uma ONG "Ação da Cidadania" cadastrada
    E existe uma ONG "Casa de Apoio" cadastrada
    Quando o Admin registra uma oferta de 4000.00
    E o Admin distribui 2000.00 para "Ação da Cidadania"
    E o Admin distribui 1500.00 para "Casa de Apoio"
    Então os membros podem visualizar a distribuição completa
    E o total distribuído é 3500.00
