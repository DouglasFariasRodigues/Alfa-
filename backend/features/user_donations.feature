# language: pt
Funcionalidade: Usuário/Membro realiza doações e ofertas

  Cenário: Usuário faz doação para a igreja
    Dado que existe um usuário "Paulo" cadastrado
    E existe um grupo "Missões" cadastrado
    E existe um membro vinculado ao usuário "Paulo"
    Quando o usuário "Paulo" realiza uma doação de 150.00 para o grupo "Missões"
    Então a doação deve ser registrada com sucesso
    E a doação deve estar vinculada ao membro de "Paulo"
    E o valor da doação deve ser 150.00

  Cenário: Usuário contribui com oferta
    Dado que existe um usuário "Maria" cadastrado
    E existe um membro vinculado ao usuário "Maria"
    Quando o usuário "Maria" realiza uma oferta de 200.00
    Então a oferta deve ser registrada
    E a oferta deve ter valor 200.00
    E a oferta deve estar visível publicamente

  Cenário: Membro visualiza histórico de doações
    Dado que existe um membro ativo "Carlos"
    E existe um grupo "Construção" cadastrado
    E o membro "Carlos" fez 5 doações para o grupo "Construção"
    Quando o membro "Carlos" consulta seu histórico de doações
    Então o membro deve ver 5 doações registradas

  Cenário: Membro faz múltiplas doações para grupos diferentes
    Dado que existe um membro ativo "Ana"
    E existe um grupo "Missões" cadastrado
    E existe um grupo "Crianças" cadastrado
    Quando o membro "Ana" doa 100.00 para "Missões"
    E o membro "Ana" doa 80.00 para "Crianças"
    Então o membro "Ana" deve ter 2 doações registradas
    E o total doado deve ser 180.00
