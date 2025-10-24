#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from django.contrib.auth.hashers import make_password, check_password

def fix_password_issues():
    print('🔧 CORRIGINDO PROBLEMAS DE SENHA')
    print('=' * 50)

    # 1. Definir senhas para membros sem senha
    print('\n🙋 CORRIGINDO MEMBROS:')
    membros_sem_senha = Membro.objects.filter(senha__isnull=True)
    
    for membro in membros_sem_senha:
        # Criar senha baseada no nome
        senha_simples = f"{membro.nome.lower().replace(' ', '')}123"
        membro.senha = make_password(senha_simples)
        membro.save()
        print(f'✅ {membro.nome}: senha definida como "{senha_simples}"')

    # 2. Verificar senhas corrompidas (hash duplo)
    print('\n🔍 VERIFICANDO SENHAS CORROMPIDAS:')
    
    # Verificar admins
    for admin in Admin.objects.all():
        if admin.senha and not admin.senha.startswith('pbkdf2_'):
            print(f'⚠️  Admin {admin.nome}: senha não hasheada')
            admin.senha = make_password('admin123')
            admin.save()
            print(f'✅ Admin {admin.nome}: senha corrigida')
    
    # Verificar membros
    for membro in Membro.objects.exclude(senha__isnull=True):
        if membro.senha and not membro.senha.startswith('pbkdf2_'):
            print(f'⚠️  Membro {membro.nome}: senha não hasheada')
            senha_simples = f"{membro.nome.lower().replace(' ', '')}123"
            membro.senha = make_password(senha_simples)
            membro.save()
            print(f'✅ Membro {membro.nome}: senha corrigida')

    # 3. Testar logins
    print('\n🧪 TESTANDO LOGINS:')
    
    # Testar admin
    try:
        admin = Admin.objects.get(email='admin@igreja.com')
        if check_password('admin123', admin.senha):
            print('✅ Login Admin: FUNCIONANDO')
        else:
            print('❌ Login Admin: NÃO FUNCIONA')
    except Exception as e:
        print(f'❌ Erro admin: {e}')
    
    # Testar membros
    for membro in Membro.objects.all():
        if membro.senha:
            senha_teste = f"{membro.nome.lower().replace(' ', '')}123"
            if check_password(senha_teste, membro.senha):
                print(f'✅ Login {membro.nome}: FUNCIONANDO (senha: {senha_teste})')
            else:
                print(f'❌ Login {membro.nome}: NÃO FUNCIONA')

    print('\n🎉 CORREÇÕES CONCLUÍDAS!')
    print('\n📋 CREDENCIAIS ATUALIZADAS:')
    print('👑 Admin: admin@igreja.com / admin123')
    for membro in Membro.objects.all():
        if membro.senha:
            senha = f"{membro.nome.lower().replace(' ', '')}123"
            print(f'🙋 {membro.nome}: {membro.email} / {senha}')

if __name__ == "__main__":
    fix_password_issues()

