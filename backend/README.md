# 🏛️ Backend - Sistema Alfa

API REST completa para gerenciamento eclesiástico, desenvolvida com **Django REST Framework**.

## 🚀 Início Rápido

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar dados de teste
python manage.py create_test_data

# Executar servidor
python manage.py runserver
```

## 📋 Funcionalidades

### 👥 Gerenciamento de Membros
- ✅ CRUD completo de membros
- ✅ Controle de status (ativo, inativo, falecido, afastado)
- ✅ Upload de documentos
- ✅ Geração de carteira de membro (PDF)
- ✅ Transferências entre igrejas

### 📅 Gerenciamento de Eventos
- ✅ Criação e edição de eventos
- ✅ Upload de fotos dos eventos
- ✅ Controle de organizadores
- ✅ Calendário de eventos

### 💰 Sistema Financeiro
- ✅ Controle de ofertas e doações
- ✅ Transações detalhadas
- ✅ Relatórios financeiros
- ✅ Categorização de receitas/despesas

### 📝 Sistema de Postagens
- ✅ Criação de postagens
- ✅ Upload de imagens
- ✅ Controle de permissões por cargo

### 👨‍💼 Gerenciamento de Usuários
- ✅ Sistema de cargos e permissões
- ✅ Autenticação JWT
- ✅ Controle de acesso baseado em roles

## 🛠️ Tecnologias

- **Django 5.0** - Framework web Python
- **Django REST Framework** - API REST
- **JWT Authentication** - Autenticação segura
- **SQLite** - Banco de dados (desenvolvimento)
- **WeasyPrint** - Geração de PDFs
- **CORS** - Cross-Origin Resource Sharing
- **Behave** - Testes BDD

## 📁 Estrutura do Projeto

```
backend/
├── alfa_project/              # Configurações do projeto
│   ├── settings.py           # Configurações Django
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # WSGI config
│   └── templates/           # Templates HTML
├── app_alfa/                # App principal
│   ├── models.py           # Modelos de dados
│   ├── serializers.py      # Serializers DRF
│   ├── viewsets.py         # ViewSets da API
│   ├── views.py            # Views tradicionais
│   ├── admin.py            # Admin Django
│   ├── management/         # Comandos customizados
│   │   └── commands/
│   │       └── create_test_data.py
│   ├── migrations/         # Migrações do banco
│   └── tests/              # Testes
├── features/               # Testes BDD (Behave)
│   ├── *.feature          # Cenários de teste
│   └── steps/             # Implementações dos steps
├── logs/                  # Logs da aplicação
├── manage.py             # Script de gerenciamento
├── requirements.txt      # Dependências Python
└── db.sqlite3           # Banco de dados
```

## 🔌 API Endpoints

### Autenticação
```
POST /api/auth/login/     # Login de usuário
POST /api/auth/logout/    # Logout de usuário
```

### Membros
```
GET    /api/membros/           # Listar membros
POST   /api/membros/           # Criar membro
GET    /api/membros/{id}/      # Obter membro
PUT    /api/membros/{id}/      # Atualizar membro
DELETE /api/membros/{id}/      # Deletar membro
```

### Eventos
```
GET    /api/eventos/           # Listar eventos
POST   /api/eventos/           # Criar evento
GET    /api/eventos/{id}/      # Obter evento
PUT    /api/eventos/{id}/      # Atualizar evento
DELETE /api/eventos/{id}/      # Deletar evento
```

### Transações
```
GET    /api/transacoes/        # Listar transações
POST   /api/transacoes/        # Criar transação
GET    /api/transacoes/{id}/   # Obter transação
PUT    /api/transacoes/{id}/   # Atualizar transação
DELETE /api/transacoes/{id}/   # Deletar transação
```

### Postagens
```
GET    /api/postagens/         # Listar postagens
POST   /api/postagens/         # Criar postagem
GET    /api/postagens/{id}/    # Obter postagem
PUT    /api/postagens/{id}/    # Atualizar postagem
DELETE /api/postagens/{id}/    # Deletar postagem
```

## 🔐 Autenticação JWT

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

### Criar Dados de Teste
```bash
python manage.py create_test_data
```

### Dados Criados
- **Admin:** `admin@igreja.com` / `admin123`
- **Cargo:** Administrador
- **Membro:** João Silva (exemplo)
- **Evento:** Culto de Domingo (exemplo)
- **Transação:** Oferta (exemplo)

## 🔧 Comandos Úteis

### Migrações
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Ver status das migrações
python manage.py showmigrations
```

### Usuários
```bash
# Criar superusuário
python manage.py createsuperuser

# Listar usuários
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.all())"
```

### Banco de Dados
```bash
# Shell interativo
python manage.py shell

# Backup do banco
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json
```

### Arquivos Estáticos
```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Limpar cache
python manage.py clear_cache
```

## 🧪 Testes

### Testes Unitários (Django)
```bash
# Todos os testes
python manage.py test

# Teste específico
python manage.py test tests.test_app.TestMembro.test_create_membro

# Com cobertura
python manage.py test --verbosity=2
```

### Testes BDD (Behave)
```bash
# Todos os testes BDD
python -m behave

# Teste específico
python -m behave features/login.feature

# Com relatório HTML
python -m behave --format html --out reports.html
```

### Estrutura dos Testes BDD
```
features/
├── login.feature                    # Cenários de login
├── admin_management.feature         # Gerenciamento de admin
├── register_members.feature         # Cadastro de membros
├── manage_members_status.feature    # Status de membros
├── manage_cargos.feature           # Gerenciamento de cargos
├── manage_ofertas.feature          # Gerenciamento de ofertas
├── event_photos.feature            # Fotos de eventos
├── publish_event_photos.feature    # Publicação de fotos
├── user_donations.feature          # Doações de usuários
├── user_view_content.feature       # Visualização de conteúdo
└── admin_full_access.feature       # Acesso completo de admin
```

## 📊 Modelos de Dados

### Principais Modelos
- **Admin** - Administradores do sistema
- **Cargo** - Cargos e permissões
- **Usuario** - Usuários do sistema
- **Membro** - Membros da igreja
- **Evento** - Eventos e atividades
- **Postagem** - Postagens e notícias
- **Transacao** - Transações financeiras
- **Oferta** - Ofertas e doações
- **Igreja** - Informações da igreja
- **ONG** - Organizações parceiras

### Relacionamentos
- Membro → Cargo (ForeignKey)
- Evento → Admin (ForeignKey - organizador)
- Postagem → Admin (ForeignKey - autor)
- Transacao → Admin (ForeignKey - registrado por)
- Oferta → Admin (ForeignKey - registrado por)

## 🔒 Segurança

### Configurações de Segurança
- **CORS** configurado para frontend
- **JWT** com tokens seguros
- **CSRF** protection habilitado
- **XSS** protection habilitado
- **SQL Injection** protection (ORM Django)

### Permissões
- **IsAuthenticated** - Usuário deve estar logado
- **IsAdminUser** - Apenas administradores
- **Custom Permissions** - Baseadas em cargos

## 📈 Performance

### Otimizações
- **select_related** - Reduz queries N+1
- **prefetch_related** - Otimiza relacionamentos
- **Database Indexing** - Índices em campos importantes
- **Caching** - Cache de queries frequentes

### Monitoramento
- **Logs** em `logs/django.log`
- **Debug Toolbar** (desenvolvimento)
- **Database Queries** logging

## 🚀 Deploy

### Configurações de Produção
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['seudominio.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alfa_db',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Servidor Web
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar com Gunicorn
gunicorn alfa_project.wsgi:application --bind 0.0.0.0:8000
```

### Nginx
```nginx
server {
    listen 80;
    server_name seudominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/static/;
    }
}
```

## 📞 Suporte

Para dúvidas sobre o backend:
- Abra uma issue no GitHub
- Consulte a documentação da API
- Entre em contato com a equipe

---

**API robusta e segura para gestão eclesiástica** 🏛️
