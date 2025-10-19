# 🎨 Frontend - Sistema Alfa

Interface moderna e responsiva para o sistema de gerenciamento eclesiástico, desenvolvida com **React + TypeScript**.

## 🚀 Início Rápido

```bash
# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev

# Build para produção
npm run build
```

## 📋 Pré-requisitos

- **Node.js 16+**
- **npm** ou **yarn**
- Backend Django rodando em `http://localhost:8000`

## 🛠️ Tecnologias Utilizadas

- **React 18** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS utilitário
- **Radix UI** - Componentes acessíveis
- **React Query** - Gerenciamento de estado e cache
- **Axios** - Cliente HTTP
- **React Router** - Roteamento
- **Lucide React** - Ícones

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── components/           # Componentes React
│   │   ├── auth/            # Autenticação
│   │   │   ├── LoginForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── layout/          # Layout da aplicação
│   │   │   ├── AppHeader.tsx
│   │   │   ├── AppSidebar.tsx
│   │   │   └── AppLayout.tsx
│   │   └── ui/              # Componentes de UI reutilizáveis
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       ├── table.tsx
│   │       └── ...
│   ├── hooks/               # Hooks personalizados
│   │   ├── useAuth.ts       # Autenticação
│   │   ├── useMembros.ts    # Gerenciamento de membros
│   │   ├── useEventos.ts    # Gerenciamento de eventos
│   │   ├── useTransacoes.ts # Gerenciamento de transações
│   │   └── usePostagens.ts  # Gerenciamento de postagens
│   ├── lib/                 # Utilitários e configurações
│   │   ├── api.ts          # Cliente Axios configurado
│   │   └── utils.ts        # Funções utilitárias
│   ├── pages/              # Páginas da aplicação
│   │   ├── Dashboard.tsx   # Dashboard principal
│   │   ├── Login.tsx       # Página de login
│   │   ├── Membros.tsx     # Gerenciamento de membros
│   │   ├── Eventos.tsx     # Gerenciamento de eventos
│   │   ├── Financas.tsx    # Sistema financeiro
│   │   └── ...
│   ├── App.tsx             # Componente principal
│   ├── main.tsx            # Ponto de entrada
│   └── index.css           # Estilos globais
├── public/                 # Arquivos estáticos
├── package.json           # Dependências e scripts
├── vite.config.ts         # Configuração Vite
├── tailwind.config.ts     # Configuração Tailwind
└── tsconfig.json          # Configuração TypeScript
```

## 🎯 Funcionalidades Implementadas

### ✅ Autenticação
- Login com JWT
- Rotas protegidas
- Logout automático
- Interceptação de tokens

### ✅ Dashboard
- Estatísticas em tempo real
- Gráficos de dados
- Atividades recentes
- Ações rápidas

### ✅ Gerenciamento de Membros
- Listagem com filtros
- Busca por nome/email/telefone
- Status (ativo, inativo, falecido, afastado)
- Estatísticas dinâmicas

### ✅ Gerenciamento de Eventos
- Listagem de eventos
- Busca por título/descrição
- Filtros por data
- Informações organizacionais

### ✅ Sistema Financeiro
- Transações detalhadas
- Gráficos de categorias
- Cálculos automáticos
- Filtros por tipo

### ✅ Sistema de Postagens
- Listagem de postagens
- Criação e edição
- Upload de imagens
- Controle de permissões

## 🔧 Scripts Disponíveis

```bash
# Desenvolvimento
npm run dev          # Servidor de desenvolvimento

# Build
npm run build        # Build para produção
npm run preview      # Preview do build

# Qualidade de código
npm run lint         # ESLint
npm run type-check   # Verificação de tipos TypeScript

# Testes
npm test             # Executar testes
npm run test:watch   # Testes em modo watch
```

## 🌐 Configuração da API

O cliente API está configurado em `src/lib/api.ts`:

```typescript
// Configuração base
const API_BASE_URL = 'http://localhost:8000/api'

// Interceptors para JWT
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 🎨 Sistema de Design

### Cores Principais
- **Primária:** Azul (#3B82F6)
- **Secundária:** Verde (#10B981)
- **Aviso:** Amarelo (#F59E0B)
- **Erro:** Vermelho (#EF4444)
- **Sucesso:** Verde (#10B981)

### Componentes UI
Todos os componentes seguem o design system do Radix UI com customizações Tailwind:

```tsx
// Exemplo de uso
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

<Button variant="primary" size="lg">
  Salvar
</Button>
```

## 📱 Responsividade

O sistema é totalmente responsivo com breakpoints:

- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

## 🔐 Autenticação

### Fluxo de Login
1. Usuário insere credenciais
2. Requisição para `/api/auth/login/`
3. Recebe JWT tokens
4. Tokens armazenados no localStorage
5. Redirecionamento para dashboard

### Rotas Protegidas
```tsx
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

## 📊 Gerenciamento de Estado

Utilizamos **React Query** para:

- Cache de dados da API
- Sincronização automática
- Loading states
- Tratamento de erros
- Invalidação de cache

### Exemplo de Hook
```tsx
export const useMembros = (filters?: MembroFilters) => {
  return useQuery({
    queryKey: ['membros', filters],
    queryFn: () => apiClient.get('/membros/', { params: filters }),
    staleTime: 5 * 60 * 1000, // 5 minutos
  })
}
```

## 🧪 Testes

### Configuração
```bash
# Instalar dependências de teste
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

### Executar Testes
```bash
npm test                 # Todos os testes
npm run test:watch      # Modo watch
npm run test:coverage   # Com cobertura
```

## 🚀 Deploy

### Build de Produção
```bash
npm run build
```

### Variáveis de Ambiente
Crie um arquivo `.env.production`:

```env
VITE_API_BASE_URL=https://api.seudominio.com
VITE_APP_NAME=Sistema Alfa
```

### Servidor Web
Configure Nginx para servir os arquivos estáticos:

```nginx
server {
    listen 80;
    server_name seudominio.com;
    root /path/to/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 🐛 Debugging

### DevTools
- **React DevTools** - Inspecionar componentes
- **React Query DevTools** - Monitorar cache e queries
- **Redux DevTools** - Gerenciamento de estado

### Logs
```typescript
// Habilitar logs detalhados
localStorage.setItem('debug', 'true')
```

## 📈 Performance

### Otimizações Implementadas
- **Code Splitting** - Carregamento sob demanda
- **Lazy Loading** - Componentes carregados quando necessário
- **Memoização** - React.memo e useMemo
- **Virtual Scrolling** - Para listas grandes
- **Image Optimization** - Lazy loading de imagens

### Bundle Analysis
```bash
npm run build -- --analyze
```

## 🤝 Contribuição

### Padrões de Código
- **ESLint** - Linting automático
- **Prettier** - Formatação de código
- **TypeScript** - Tipagem estática
- **Conventional Commits** - Padrão de commits

### Estrutura de Commits
```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: formatação de código
refactor: refatoração
test: adiciona testes
chore: tarefas de manutenção
```

## 📞 Suporte

Para dúvidas sobre o frontend:
- Abra uma issue no GitHub
- Consulte a documentação dos componentes
- Entre em contato com a equipe

---

**Interface moderna e intuitiva para gestão eclesiástica** 🎨
