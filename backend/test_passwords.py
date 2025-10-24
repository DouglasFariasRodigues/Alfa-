#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from django.contrib.auth.hashers import check_password, make_password

def test_password_system():
    print('🔍 TESTANDO SISTEMA DE SENHAS')
    print('=' * 50)

    # Verificar Admin
    print('\n👑 ADMIN:')
    admin = Admin.objects.first()
    if admin:
        print(f'Nome: {admin.nome}')
        print(f'Email: {admin.email}')
        print(f'Senha hash: {admin.senha[:20]}...')
        
        # Testar senha
        senha_teste = 'admin123'
        if check_password(senha_teste, admin.senha):
            print('✅ Senha admin123: VÁLIDA')
        else:
            print('❌ Senha admin123: INVÁLIDA')
            
        # Testar senha incorreta
        if check_password('senhaerrada', admin.senha):
            print('✅ Senha senhaerrada: VÁLIDA')
        else:
            print('❌ Senha senhaerrada: INVÁLIDA (correto)')

    # Verificar Membro
    print('\n🙋 MEMBRO:')
    membro = Membro.objects.first()
    if membro:
        print(f'Nome: {membro.nome}')
        print(f'Email: {membro.email}')
        print(f'Senha hash: {membro.senha[:20] if membro.senha else "SEM SENHA"}...')
        
        if membro.senha:
            # Testar senha
            senha_teste = 'senha123'
            if check_password(senha_teste, membro.senha):
                print('✅ Senha senha123: VÁLIDA')
            else:
                print('❌ Senha senha123: INVÁLIDA')
        else:
            print('⚠️  MEMBRO SEM SENHA DEFINIDA')
            
    # Testar criação de nova senha
    print('\n🧪 TESTANDO CRIAÇÃO DE SENHA:')
    try:
        # Criar senha de teste
        senha_teste = 'teste123'
        senha_hash = make_password(senha_teste)
        print(f'Senha hash gerada: {senha_hash[:20]}...')
        
        # Verificar se a senha funciona
        if check_password(senha_teste, senha_hash):
            print('✅ Hash de senha funciona corretamente')
        else:
            print('❌ Hash de senha NÃO funciona')
            
    except Exception as e:
        print(f'❌ Erro ao testar hash: {e}')

if __name__ == "__main__":
    test_password_system()

