# language: pt
Funcionalidade: Validação de Expiração de JWT Token

  Cenário: Token expirado é rejeitado
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin recebe um access_token válido
    E o token expira (simula passagem de tempo)
    Quando o Admin tenta acessar a API com o token expirado
    Então a requisição deve retornar erro 401 "Unauthorized"

  Cenário: Token válido funciona normalmente
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin recebe um access_token válido
    Quando o Admin tenta acessar a API com o token válido
    Então a requisição deve retornar status 200
    E o Admin deve receber os dados de resposta
