# language: pt
Funcionalidade: Refresh Token JWT

  Cenário: Renovar token expirado com refresh token
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin recebe um access_token e refresh_token válidos
    Quando o Admin usa o refresh_token para renovar o access_token
    Então o Admin deve receber um novo access_token válido
    E o novo access_token deve permitir requisições à API

  Cenário: Refresh token inválido é rejeitado
    Quando o Admin tenta usar um refresh_token inválido
    Então a requisição deve retornar erro 401 "Unauthorized"

  Cenário: Novo token tem tempo de expiração atualizado
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin recebe um access_token e refresh_token válidos
    Quando o Admin usa o refresh_token para renovar o access_token
    Então o novo access_token deve ter uma data de expiração 60 minutos no futuro
