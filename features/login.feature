# language: pt
Funcionalidade: Login do Admin

  Cenário: Login bem-sucedido com credenciais válidas
    Dado que existe um Admin com email "admin@example.com" e senha "password123"
    Quando eu tento fazer login com email "admin@example.com" e senha "password123"
    Então eu devo estar logado com sucesso

  Cenário: Login falha com credenciais inválidas
    Dado que existe um Admin com email "admin@example.com" e senha "password123"
    Quando eu tento fazer login com email "admin@example.com" e senha "wrongpassword"
    Então eu devo ver uma mensagem de erro de login
