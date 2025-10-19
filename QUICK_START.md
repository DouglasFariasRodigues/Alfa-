# 🚀 Guia de Início Rápido - Sistema Alfa

## ⚡ Execução Rápida (5 minutos)

### 1. Backend (Django)
```bash
# Navegar para o backend
cd backend

# Ativar ambiente virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Executar servidor
python manage.py runserver
```
**✅ Backend rodando em:** `http://localhost:8000`

### 2. Frontend (React)
```bash
# Navegar para o frontend (nova janela)
cd frontend

# Executar servidor
npm run dev
```
**✅ Frontend rodando em:** `http://localhost:8080`

### 3. Acessar o Sistema
1. Abra: `http://localhost:8080`
2. Login: `admin@igreja.com`
3. Senha: `admin123`

---

## 🔧 Se for a primeira vez

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_test_data
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📱 URLs Importantes

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/
- **API Docs:** http://localhost:8000/api/

---

## 🆘 Problemas Comuns

### Backend não inicia
```bash
# Verificar se está no diretório correto
cd backend
ls manage.py  # Deve existir

# Ativar ambiente virtual
venv\Scripts\activate

# Verificar dependências
pip list
```

### Frontend não inicia
```bash
# Verificar se está no diretório correto
cd frontend
ls package.json  # Deve existir

# Instalar dependências
npm install

# Limpar cache
npm cache clean --force
```

### Erro de CORS
- Verificar se backend está rodando na porta 8000
- Verificar configuração CORS em `backend/alfa_project/settings.py`

### Erro de autenticação
- Verificar se dados de teste foram criados: `python manage.py create_test_data`
- Usar credenciais: `admin@igreja.com` / `admin123`

---

## 📞 Suporte Rápido

- **Backend não funciona:** Verificar se `manage.py` existe e ambiente virtual ativo
- **Frontend não funciona:** Verificar se `package.json` existe e `npm install` executado
- **Login não funciona:** Executar `python manage.py create_test_data`
- **Erro 500:** Verificar logs em `backend/logs/django.log`

---

**Sistema funcionando em menos de 5 minutos!** ⚡
