# language: pt
Funcionalidade: Gerenciar cargos da igreja

  Cenário: Admin cria um novo cargo
    Dado que existe um Admin logado
    Quando o Admin cria o cargo "Pastor" com descrição "Líder espiritual da congregação"
    Então o cargo "Pastor" deve estar cadastrado
    E o cargo deve ter sido criado pelo Admin

  Cenário: Admin cria múltiplos cargos
    Dado que existe um Admin logado
    Quando o Admin cria o cargo "Diácono" com descrição "Auxiliar no ministério"
    E o Admin cria o cargo "Líder de Louvor" com descrição "Responsável pelo louvor"
    E o Admin cria o cargo "Tesoureiro" com descrição "Gerencia as finanças"
    Então devem existir 3 cargos cadastrados

  Cenário: Admin visualiza todos os cargos cadastrados
    Dado que existe um Admin logado
    E existe o cargo "Pastor" cadastrado
    E existe o cargo "Diácono" cadastrado
    Quando o Admin solicita visualizar todos os cargos
    Então o Admin deve ver 2 cargos listados
