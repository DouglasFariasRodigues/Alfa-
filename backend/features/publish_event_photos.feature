# language: pt
Funcionalidade: Publicar artes e fotos de eventos

  Cenário: Admin publica fotos de um evento
    Dado que existe um Admin logado
    E existe um evento "Culto de Páscoa"
    Quando o Admin publica 3 fotos para o evento "Culto de Páscoa"
    Então o evento deve ter 3 fotos publicadas

  Cenário: Admin publica múltiplas fotos em eventos diferentes
    Dado que existe um Admin logado
    E existe um evento "Culto de Natal"
    E existe um evento "Batismo"
    Quando o Admin publica 2 fotos para o evento "Culto de Natal"
    E o Admin publica 4 fotos para o evento "Batismo"
    Então o evento "Culto de Natal" deve ter 2 fotos
    E o evento "Batismo" deve ter 4 fotos

  Cenário: Admin publica postagem com fotos dos eventos
    Dado que existe um Admin logado como usuário
    Quando o Admin cria uma postagem "Momentos Especiais" com 3 fotos
    Então a postagem "Momentos Especiais" deve estar publicada
    E a postagem deve ter 3 fotos anexadas
