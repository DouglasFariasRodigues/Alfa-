# language: pt
Funcionalidade: Cadastrar e gerenciar membros

  Cenário: Admin cadastra novo membro com dados pessoais
    Dado que existe um Admin logado
    Quando o Admin cadastra um membro com os seguintes dados:
      | nome          | João da Silva    |
      | cpf           | 123.456.789-00   |
      | email         | joao@email.com   |
      | telefone      | (11) 98765-4321  |
      | data_batismo  | 2024-01-15       |
    Então o membro "João da Silva" deve estar cadastrado
    E o membro deve ter sido cadastrado pelo Admin
    E os dados devem estar armazenados de forma segura

  Cenário: Admin gera cartão de membro automaticamente
    Dado que existe um Admin logado
    E existe um membro cadastrado "Maria Santos"
    Quando o Admin gera um cartão de membro para "Maria Santos"
    Então o documento do tipo "cartao_membro" deve ser gerado
    E o documento deve estar vinculado ao membro "Maria Santos"

  Cenário: Admin gera transferência de igreja
    Dado que existe um Admin logado
    E existe um membro cadastrado "Pedro Oliveira"
    Quando o Admin gera transferência de igreja para "Pedro Oliveira"
    Então o documento do tipo "transferencia" deve ser gerado
    E o documento deve estar vinculado ao membro "Pedro Oliveira"

  Cenário: Admin gera registro de membro
    Dado que existe um Admin logado
    E existe um membro cadastrado "Ana Costa"
    Quando o Admin gera registro para "Ana Costa"
    Então o documento do tipo "registro" deve ser gerado
    E o documento deve ter sido gerado pelo Admin

  Cenário: Admin visualiza todos os documentos de um membro
    Dado que existe um Admin logado
    E existe um membro cadastrado "Carlos Silva"
    E o membro "Carlos Silva" tem 3 documentos gerados
    Quando o Admin consulta os documentos de "Carlos Silva"
    Então o Admin deve ver 3 documentos
