# language: pt
Funcionalidade: Visualizar fotos de eventos

  Cenário: Admin visualiza fotos de um evento com múltiplas fotos
    Dado que existe um Admin logado
    E existe um evento "Culto de Domingo" com 3 fotos
    Quando o Admin solicita visualizar as fotos do evento "Culto de Domingo"
    Então o Admin deve ver 3 fotos do evento

  Cenário: Admin visualiza evento sem fotos
    Dado que existe um Admin logado
    E existe um evento "Reunião de Oração" sem fotos
    Quando o Admin solicita visualizar as fotos do evento "Reunião de Oração"
    Então o Admin deve ver uma mensagem indicando que não há fotos

  Cenário: Admin visualiza fotos de múltiplos eventos
    Dado que existe um Admin logado
    E existe um evento "Missa de Natal" com 5 fotos
    E existe um evento "Encontro de Jovens" com 2 fotos
    Quando o Admin solicita visualizar todos os eventos com fotos
    Então o Admin deve ver 2 eventos listados
    E o evento "Missa de Natal" deve ter 5 fotos
    E o evento "Encontro de Jovens" deve ter 2 fotos
