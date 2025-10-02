# language: pt
Funcionalidade: Admin login completo

  Cenário: Admin faz login para gerenciamento completo da aplicação
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    Então o Admin deve estar autenticado
    E o Admin deve ter acesso total à aplicação

  Cenário: Admin faz login para gerenciar membros e informações
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin acessa a área de membros
    Então o Admin deve ter permissão para gerenciar membros
    E o Admin pode visualizar informações dos membros

  Cenário: Admin gerencia valores das ofertas após login
    Dado que existe um Admin autenticado
    E existe uma oferta de 1000.00 registrada
    Quando o Admin edita o valor da oferta para 1200.00
    Então a oferta deve ter valor 1200.00
    E a alteração deve ser registrada

  Cenário: Admin com permissões visualiza fotos de eventos
    Dado que existe um Admin autenticado
    E existe um evento "Culto Especial" com 4 fotos
    Quando o Admin acessa a galeria de fotos do evento "Culto Especial"
    Então o Admin deve visualizar 4 fotos
    E o Admin pode gerenciar as fotos
