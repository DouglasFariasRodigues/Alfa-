# language: pt
Funcionalidade: Usuario acessa apenas recursos permitidos por seu cargo

  @wip @known-issue
  Cenário: Usuario com cargo limitado não consegue gerenciar membros
    Dado que existe um Usuario cadastrado com email "usuario@igreja.com" e senha "senha123"
    E o Usuario tem um cargo "Organizador de Eventos" sem permissão para gerenciar membros
    Quando o Usuario tenta criar um novo membro
    # TODO: Sistema precisa implementar is_authenticated no modelo Usuario
    # Então a requisição deve retornar erro 403 "Forbidden"

  @wip @known-issue
  Cenário: Usuario com cargo adequado consegue listar eventos
    Dado que existe um Usuario cadastrado com email "usuario@igreja.com" e senha "senha123"
    E o Usuario tem um cargo "Gerenciador de Eventos" com permissão para gerenciar eventos
    Quando o Usuario tenta listar eventos
    # TODO: Sistema precisa implementar is_authenticated no modelo Usuario
    # Então a requisição deve retornar status 200
