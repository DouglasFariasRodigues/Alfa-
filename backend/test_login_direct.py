#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from django.contrib.auth.hashers import check_password

def test_login_direct():
    print('🧪 TESTANDO LOGIN DIRETO')
    print('=' * 40)

    # Testar login admin
    print('\n👑 TESTANDO LOGIN ADMIN:')
    try:
        admin = Admin.objects.get(email='admin@igreja.com')
        senha = 'admin123'
        
        if check_password(senha, admin.senha):
            print('✅ LOGIN ADMIN: SUCESSO')
            print(f'   Nome: {admin.nome}')
            print(f'   Email: {admin.email}')
        else:
            print('❌ LOGIN ADMIN: SENHA INCORRETA')
            
    except Admin.DoesNotExist:
        print('❌ LOGIN ADMIN: USUÁRIO NÃO ENCONTRADO')
    except Exception as e:
        print(f'❌ LOGIN ADMIN: ERRO - {e}')

    # Testar login membro
    print('\n🙋 TESTANDO LOGIN MEMBRO:')
    try:
        membro = Membro.objects.get(email='ana@email.com')
        
        if membro.senha:
            senha = 'senha123'
            if check_password(senha, membro.senha):
                print('✅ LOGIN MEMBRO: SUCESSO')
                print(f'   Nome: {membro.nome}')
                print(f'   Email: {membro.email}')
            else:
                print('❌ LOGIN MEMBRO: SENHA INCORRETA')
        else:
            print('⚠️  LOGIN MEMBRO: SEM SENHA DEFINIDA')
            print('   Precisa definir senha para o membro')
            
    except Membro.DoesNotExist:
        print('❌ LOGIN MEMBRO: USUÁRIO NÃO ENCONTRADO')
    except Exception as e:
        print(f'❌ LOGIN MEMBRO: ERRO - {e}')

    # Verificar problemas comuns
    print('\n🔍 DIAGNÓSTICO:')
    
    # Verificar se há senhas não hasheadas
    admins_sem_hash = Admin.objects.exclude(senha__startswith='pbkdf2_')
    if admins_sem_hash.exists():
        print(f'⚠️  {admins_sem_hash.count()} Admins com senhas não hasheadas')
    
    membros_sem_hash = Membro.objects.exclude(senha__startswith='pbkdf2_').exclude(senha__isnull=True)
    if membros_sem_hash.exists():
        print(f'⚠️  {membros_sem_hash.count()} Membros com senhas não hasheadas')
    
    # Verificar senhas vazias
    membros_sem_senha = Membro.objects.filter(senha__isnull=True)
    if membros_sem_senha.exists():
        print(f'⚠️  {membros_sem_senha.count()} Membros sem senha')

if __name__ == "__main__":
    test_login_direct()

