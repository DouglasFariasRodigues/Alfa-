# 🎭 BDD Tests - Behave Features

Testes BDD organizados em 3 níveis: **Integration** e **E2E**.

## 📁 Estrutura

```
bdd/
├── integration/          # Testes com banco de dados
│   ├── auth/            # Autenticação e JWT
│   ├── members/         # Gerenciamento de membros
│   ├── finance/         # Ofertas e doações
│   ├── events/          # Eventos e fotos
│   └── content/         # Visualização de conteúdo
├── e2e/                 # Testes End-to-End
│   ├── auth/            # Permissões de usuários
│   └── flows/           # Fluxos completos
├── steps/               # Steps compartilhados consolidados
│   ├── auth_steps.py
│   ├── jwt_steps.py
│   ├── members_steps.py
│   ├── finance_steps.py
│   ├── events_steps.py
│   ├── content_steps.py
│   ├── admin_steps.py
│   ├── cargos_steps.py
│   └── usuario_steps.py
├── environment.py       # Setup/teardown global
└── behave.ini          # Configuração do Behave
```

## 🚀 Como Rodar

### Rodar Todos os Testes BDD
```bash
cd bdd
behave
```

### Rodar por Nível
```bash
# Integration (com banco)
behave integration/

# E2E (fluxos completos)
behave e2e/
```

### Rodar por Categoria
```bash
# Autenticação
behave integration/auth/ e2e/auth/

# Membros
behave integration/members/

# Finanças
behave integration/finance/

# Eventos
behave integration/events/

# Conteúdo
behave integration/content/

# Fluxos completos
behave e2e/flows/
```

### Rodar com Tags
```bash
# Tags devem ser adicionadas aos features
behave --tags=@auth
behave --tags=@integration
behave --tags=@e2e
```

### Com Verbosidade
```bash
behave -v              # Verbose
behave --no-capture    # Sem captura de output
behave --format plain  # Formato texto
```

## 📝 Estrutura de um Feature File

```gherkin
# language: pt
Funcionalidade: Login do Admin

  @integration @auth
  Cenário: Login bem-sucedido com credenciais válidas
    Dado que existe um Admin com email "admin@example.com" e senha "password123"
    Quando eu tento fazer login com email "admin@example.com" e senha "password123"
    Então eu devo estar logado com sucesso

  @integration @auth
  Cenário: Login falha com credenciais inválidas
    Dado que existe um Admin com email "admin@example.com" e senha "password123"
    Quando eu tento fazer login com email "admin@example.com" e senha "wrongpassword"
    Então eu devo ver uma mensagem de erro de login
```

## 📂 Organização por Tipo

### Integration Tests (`integration/`)
- **Propósito**: Testa fluxos com banco de dados
- **Escopo**: Um domínio específico (membros, finanças, etc)
- **Duração**: Rápidos (< 5s cada)
- **Setup**: Cria dados de teste, não limpa automaticamente

### E2E Tests (`e2e/`)
- **Propósito**: Testa fluxos completos de usuário
- **Escopo**: Múltiplos domínios interagindo
- **Duração**: Podem ser lentos
- **Setup**: Pode usar Selenium para testar UI

## 🔧 Consolidação de Steps

Os steps foram consolidados por domínio para evitar duplicação:

| File | Features |
|------|----------|
| `auth_steps.py` | Login, autenticação |
| `jwt_steps.py` | JWT tokens, refresh |
| `members_steps.py` | Registro e status de membros |
| `finance_steps.py` | Ofertas e doações |
| `events_steps.py` | Eventos e fotos |
| `content_steps.py` | Visualização de conteúdo |
| `admin_steps.py` | Permissões de admin |
| `cargos_steps.py` | Gerenciamento de cargos |
| `usuario_steps.py` | Permissões de usuários |

## 🎯 Próximas Etapas

1. Adicionar tags `@integration` e `@e2e` aos features
2. Consolidar steps duplicados
3. Atualizar `environment.py` com fixtures compartilhadas
4. Integrar com CI/CD (rodar antes de pytest)
5. Remover pasta `features/` antiga (após migração completa)

## 📖 Referências

- [Behave Documentation](https://behave.readthedocs.io/)
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
- [BDD Best Practices](https://cucumber.io/docs/bdd/)
