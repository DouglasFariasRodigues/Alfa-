# language: pt
Funcionalidade: Usuário/Membro visualiza fotos e ofertas

  Cenário: Usuário visualiza fotos de eventos
    Dado que existe um usuário "João" cadastrado
    E existe um evento "Missa Dominical" com 5 fotos públicas
    Quando o usuário "João" solicita visualizar as fotos do evento "Missa Dominical"
    Então o usuário deve ver 5 fotos

  Cenário: Usuário visualiza fotos de postagens da igreja
    Dado que existe um usuário "Maria" cadastrado
    E existe uma postagem "Encontro de Jovens 2025" com 4 fotos
    Quando o usuário "Maria" solicita visualizar a postagem "Encontro de Jovens 2025"
    Então o usuário deve ver a postagem com 4 fotos

  Cenário: Usuário visualiza ofertas e destino do dinheiro
    Dado que existe um usuário "Pedro" cadastrado
    E existe uma oferta pública de 3000.00 distribuída para ONGs
    Quando o usuário "Pedro" solicita visualizar as ofertas públicas
    Então o usuário deve ver pelo menos 1 oferta
    E o usuário deve ver as distribuições da oferta

  Cenário: Membro visualiza transparência das ofertas
    Dado que existe um membro ativo na igreja
    E existe uma oferta de 5000.00 com 3 distribuições para diferentes ONGs
    Quando o membro solicita visualizar a transparência das ofertas
    Então o membro deve ver a oferta com valor 5000.00
    E o membro deve ver 3 destinos da oferta
