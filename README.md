# 🏛️ Sistema de Gerenciamento Eclesiástico - Alfa

Sistema completo de gerenciamento para igrejas, desenvolvido com **Django REST Framework** (backend) e **React + TypeScript** (frontend).

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Autenticação](#-autenticação)
- [Dados de Teste](#-dados-de-teste)
- [Desenvolvimento](#-desenvolvimento)
- [Testes](#-testes)

## 🚀 Funcionalidades

### 👥 Gerenciamento de Membros
- ✅ Cadastro completo de membros com documentos
- ✅ Controle de status (ativo, inativo, falecido, afastado)
- ✅ Geração automática de carteira de membro
- ✅ Transferências entre igrejas

### 📅 Gerenciamento de Eventos
- ✅ Criação e edição de eventos
- ✅ Upload de fotos dos eventos
- ✅ Controle de organizadores e participantes
- ✅ Calendário de eventos

### 💰 Sistema Financeiro
- ✅ Controle de ofertas e doações
- ✅ Transações detalhadas (entradas e saídas)
- ✅ Relatórios financeiros
- ✅ Categorização de receitas e despesas

### 📝 Sistema de Postagens
- ✅ Criação de postagens e notícias
- ✅ Upload de imagens
- ✅ Controle de permissões por cargo

### 👨‍💼 Gerenciamento de Usuários
- ✅ Sistema de cargos e permissões
- ✅ Autenticação JWT segura
- ✅ Controle de acesso baseado em roles

## 🛠️ Tecnologias

### Backend
- **Django 5.0** - Framework web Python
- **Django REST Framework** - API REST
- **JWT Authentication** - Autenticação segura
- **SQLite** - Banco de dados (desenvolvimento)
- **WeasyPrint** - Geração de PDFs
- **CORS** - Cross-Origin Resource Sharing

### Frontend
- **React 18** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS
- **Radix UI** - Componentes acessíveis
- **React Query** - Gerenciamento de estado e cache
- **Axios** - Cliente HTTP

## 📋 Pré-requisitos

- **Python 3.8+**
- **Node.js 16+**
- **npm** ou **yarn**
- **Git**

## 🔧 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone <https://github.com/DouglasFariasRodigues/Alfa->
cd Alfa-
```

### 2. Configuração do Backend

```bash
# Navegue para o diretório backend
cd backend

# Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie dados de teste (opcional)
python manage.py create_test_data
```

### 3. Configuração do Frontend

```bash
# Navegue para o diretório frontend
cd ../frontend

# Instale as dependências
npm install
```

## 🚀 Como Executar

### Desenvolvimento

#### 1. Inicie o Backend
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```
O backend estará disponível em: `http://localhost:8000`

#### 2. Inicie o Frontend
```bash
cd frontend
npm run dev
```
O frontend estará disponível em: `http://localhost:8080`

### Produção

#### Backend
```bash
cd backend
venv\Scripts\activate
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
```

#### Frontend
```bash
cd frontend
npm run build
npm run preview
```

## 📁 Estrutura do Projeto

```
Alfa-/
├── backend/                    # Django Backend
│   ├── alfa_project/          # Configurações do projeto
│   │   ├── settings.py        # Configurações Django
│   │   ├── urls.py           # URLs principais
│   │   └── wsgi.py           # WSGI config
│   ├── app_alfa/             # App principal
│   │   ├── models.py         # Modelos de dados
│   │   ├── serializers.py    # Serializers DRF
│   │   ├── viewsets.py       # ViewSets da API
│   │   ├── management/       # Comandos customizados
│   │   └── migrations/       # Migrações do banco
│   ├── manage.py             # Script de gerenciamento
│   ├── requirements.txt      # Dependências Python
│   └── db.sqlite3           # Banco de dados
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── auth/        # Componentes de autenticação
│   │   │   ├── layout/      # Layout da aplicação
│   │   │   └── ui/          # Componentes de UI
│   │   ├── hooks/           # Hooks personalizados
│   │   ├── lib/             # Utilitários e configurações
│   │   ├── pages/           # Páginas da aplicação
│   │   └── App.tsx          # Componente principal
│   ├── package.json         # Dependências Node.js
│   └── vite.config.ts       # Configuração Vite
└── README.md                # Este arquivo
```

## 🔌 API Endpoints

### Autenticação
- `POST /api/auth/login/` - Login de usuário
- `POST /api/auth/logout/` - Logout de usuário

### Membros
- `GET /api/membros/` - Listar membros
- `POST /api/membros/` - Criar membro
- `GET /api/membros/{id}/` - Obter membro
- `PUT /api/membros/{id}/` - Atualizar membro
- `DELETE /api/membros/{id}/` - Deletar membro

### Eventos
- `GET /api/eventos/` - Listar eventos
- `POST /api/eventos/` - Criar evento
- `GET /api/eventos/{id}/` - Obter evento
- `PUT /api/eventos/{id}/` - Atualizar evento
- `DELETE /api/eventos/{id}/` - Deletar evento

### Transações
- `GET /api/transacoes/` - Listar transações
- `POST /api/transacoes/` - Criar transação
- `GET /api/transacoes/{id}/` - Obter transação
- `PUT /api/transacoes/{id}/` - Atualizar transação
- `DELETE /api/transacoes/{id}/` - Deletar transação

### Postagens
- `GET /api/postagens/` - Listar postagens
- `POST /api/postagens/` - Criar postagem
- `GET /api/postagens/{id}/` - Obter postagem
- `PUT /api/postagens/{id}/` - Atualizar postagem
- `DELETE /api/postagens/{id}/` - Deletar postagem

## 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Tokens)** para autenticação:

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@igreja.com", "senha": "admin123"}'
```

### Resposta
```json
{
  "success": true,
  "message": "Login realizado com sucesso",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "nome": "Administrador",
    "email": "admin@igreja.com"
  }
}
```

### Uso do Token
```bash
curl -X GET http://localhost:8000/api/membros/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

## 🧪 Dados de Teste

Para criar dados de teste no sistema:

```bash
cd backend
python manage.py create_test_data
```

Isso criará:
- 1 usuário administrador (`admin@igreja.com` / `admin123`)
- 1 cargo padrão
- 1 membro de exemplo
- 1 evento de exemplo
- 1 transação de exemplo

## 💻 Desenvolvimento

### Comandos Úteis

#### Backend
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Shell interativo
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

#### Frontend
```bash
# Instalar dependências
npm install

# Modo desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview

# Linting
npm run lint
```

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080
```

## 🧪 Testes

### Backend (Django)

#### Testes Unitários
```bash
cd backend
python manage.py test
```

#### Testes BDD (Behave)
```bash
cd backend
python -m behave
```

#### Teste Específico
```bash
python -m behave features/login.feature
```

### Frontend (React)

```bash
cd frontend
npm test
```

## 📊 Monitoramento

### Logs do Django
Os logs são salvos em `backend/logs/django.log`

### Admin Django
Acesse `http://localhost:8000/admin/` para gerenciar dados diretamente no banco.

## 🚀 Deploy

### Backend (Django)
1. Configure variáveis de ambiente de produção
2. Use um banco de dados PostgreSQL/MySQL
3. Configure servidor web (Nginx + Gunicorn)
4. Execute `collectstatic`

### Frontend (React)
1. Execute `npm run build`
2. Sirva os arquivos estáticos com Nginx
3. Configure proxy para API


