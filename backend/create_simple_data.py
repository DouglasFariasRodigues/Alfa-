#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime

print('✅ Criando dados de teste...')

# Criar apenas Admin e Membro (sem Usuario por enquanto)
try:
    # Criar Admin
    admin = Admin.objects.create(
        nome='Pastor João',
        email='admin@igreja.com',
        telefone='11999999999',
        senha=make_password('admin123'),
        is_admin=True
    )
    print(f'👑 Admin criado: {admin.nome} ({admin.email}) - Senha: admin123')

    # Criar Membro
    membro = Membro.objects.create(
        nome='Ana Costa',
        email='ana@email.com',
        telefone='11777777777',
        cpf='12345678901',
        rg='123456789',
        data_nascimento='1990-01-01',
        cadastrado_por=admin
    )
    print(f'🙋 Membro criado: {membro.nome} ({membro.email})')

    print('\n🎉 DADOS CRIADOS COM SUCESSO!')
    print('\n📋 CREDENCIAIS DE ACESSO:')
    print('=' * 50)
    print('🔐 DJANGO ADMIN:')
    print('   URL: http://127.0.0.1:8000/admin/')
    print('   Usuário: admin')
    print('   Senha: admin123')
    print('')
    print('🔐 FRONTEND (Admin):')
    print('   URL: http://localhost:3000/')
    print('   Email: admin@igreja.com')
    print('   Senha: admin123')
    print('')
    print('🔐 FRONTEND (Membro):')
    print('   URL: http://localhost:3000/')
    print('   Email: ana@email.com')
    print('   Senha: (sem senha definida)')
    print('=' * 50)

except Exception as e:
    print(f'❌ Erro ao criar dados: {e}')
    import traceback
    traceback.print_exc()

