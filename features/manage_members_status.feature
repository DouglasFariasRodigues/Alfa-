# language: pt
Funcionalidade: Gerenciar membros por status

  Cenário: Admin visualiza quantidade de membros por status
    Dado que existe um Admin logado
    E existem 10 membros ativos cadastrados
    E existem 3 membros inativos cadastrados
    E existem 2 membros falecidos cadastrados
    E existem 5 membros afastados da fé cadastrados
    Quando o Admin solicita visualizar estatísticas de membros
    Então o Admin deve ver 10 membros ativos
    E o Admin deve ver 3 membros inativos
    E o Admin deve ver 2 membros falecidos
    E o Admin deve ver 5 membros afastados

  Cenário: Admin altera status de membro ativo para inativo
    Dado que existe um Admin logado
    E existe um membro ativo "João Silva"
    Quando o Admin altera o status de "João Silva" para inativo
    Então o membro "João Silva" deve ter status inativo

  Cenário: Admin registra membro que deixou a fé
    Dado que existe um Admin logado
    E existe um membro ativo "Maria Santos"
    Quando o Admin altera o status de "Maria Santos" para afastado
    Então o membro "Maria Santos" deve ter status afastado
    E o membro deve estar na lista de pessoas que deixaram a fé
