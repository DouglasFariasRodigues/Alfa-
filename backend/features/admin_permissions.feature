# language: pt
Funcionalidade: Admin sem permissão é bloqueado

  Cenário: Admin tenta registrar dízimo sem permissão
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    E o Admin tem um cargo "Secretário" sem permissão para registrar dízimos
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin tenta criar uma transação de entrada tipo "dízimo" com valor 500.00
    Então a requisição deve retornar erro 403 "Forbidden"
    E a mensagem de erro deve conter "permissões insuficientes"

  Cenário: Admin com permissão consegue registrar dízimo
    Dado que existe um Admin cadastrado com email "admin@igreja.com" e senha "senha123"
    E o Admin tem um cargo "Pastor" com permissão para registrar dízimos
    Quando o Admin faz login com email "admin@igreja.com" e senha "senha123"
    E o Admin tenta criar uma transação de entrada tipo "dízimo" com valor 500.00
    Então a requisição deve retornar status 201 ou 200
    E a transação deve ser criada com sucesso
