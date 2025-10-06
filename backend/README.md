# Projeto Alfa

Este é um projeto de aplicação web Django para gerenciamento eclesiástico.

## Funcionalidades

- Gerenciamento de usuários (Admin, Usuario)
- Gerenciamento de membros (Membro) com status ativo/inativo/falecido
- Rastreamento de doações (Doacao) e renda mensal das ofertas
- Informações da igreja (Igreja)
- Adição de eventos e postagens
- Grupos para quais vão as doações
- Automação de criação de documentos:
  - Carteira de membro
  - Transferências para outra igreja
- Funcionalidade de exclusão suave (soft delete)

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual: `source venv/bin/activate` (no Linux)
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute as migrações: `python manage.py migrate`
6. Execute o servidor: `python manage.py runserver`

## Uso

- Acesse o painel de administração em /admin
- Adicione membros, doações, eventos, postagens, etc.
- Gere documentos automaticamente

## Contribuição

Para contribuir, faça um fork do repositório, crie uma branch para sua feature, e envie um pull request.

## Licença

Este projeto está sob a licença MIT.
