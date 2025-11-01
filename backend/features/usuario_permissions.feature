# language: pt
Funcionalidade: Usuario acessa apenas recursos permitidos por seu cargo

  Cenário: Usuario com cargo limitado não consegue gerenciar membros
    Dado que existe um Usuario cadastrado com email "usuario@igreja.com" e senha "senha123"
    E o Usuario tem um cargo "Organizador de Eventos" sem permissão para gerenciar membros
    Quando o Usuario faz login com email "usuario@igreja.com" e senha "senha123"
    E o Usuario tenta criar um novo membro
    Então a requisição deve retornar erro 403 "Forbidden"
    E a mensagem de erro deve conter "permissões insuficientes"

  Cenário: Usuario com cargo adequado consegue gerenciar eventos
    Dado que existe um Usuario cadastrado com email "usuario@igreja.com" e senha "senha123"
    E o Usuario tem um cargo "Gerenciador de Eventos" com permissão para gerenciar eventos
    Quando o Usuario faz login com email "usuario@igreja.com" e senha "senha123"
    E o Usuario tenta listar eventos
    Então a requisição deve retornar status 200
    E o Usuario deve receber a lista de eventos
