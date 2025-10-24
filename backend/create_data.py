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

# Criar Cargos
cargo_admin = Cargo.objects.create(
    nome='Administrador',
    descricao='Acesso total ao sistema',
    pode_gerenciar_membros=True,
    pode_gerenciar_eventos=True,
    pode_gerenciar_financas=True,
    pode_gerenciar_cargos=True,
    pode_registrar_dizimos=True,
    pode_registrar_ofertas=True
)

cargo_lider = Cargo.objects.create(
    nome='Líder de Eventos',
    descricao='Pode gerenciar eventos',
    pode_gerenciar_eventos=True,
    pode_gerenciar_membros=False,
    pode_gerenciar_financas=False,
    pode_gerenciar_cargos=False,
    pode_registrar_dizimos=False,
    pode_registrar_ofertas=False
)

cargo_membro = Cargo.objects.create(
    nome='Membro',
    descricao='Membro comum',
    pode_gerenciar_eventos=False,
    pode_gerenciar_membros=False,
    pode_gerenciar_financas=False,
    pode_gerenciar_cargos=False,
    pode_registrar_dizimos=False,
    pode_registrar_ofertas=False
)

# Criar Admin
admin = Admin.objects.create(
    nome='Pastor João',
    email='admin@igreja.com',
    telefone='11999999999',
    senha=make_password('admin123'),
    cargo=cargo_admin,
    is_admin=True
)

# Criar Usuario
usuario = Usuario.objects.create(
    username='marketing',
    email='marketing@igreja.com',
    telefone='11888888888',
    senha=make_password('marketing123'),
    cargo=cargo_lider
)

# Criar Membros
membro1 = Membro.objects.create(
    nome='Ana Costa',
    email='ana@email.com',
    telefone='11777777777',
    cpf='12345678901',
    rg='123456789',
    data_nascimento='1990-01-01',
    cargo=cargo_lider,
    cadastrado_por=admin
)

membro2 = Membro.objects.create(
    nome='Carlos Silva',
    email='carlos@email.com',
    telefone='11666666666',
    cpf='98765432100',
    rg='987654321',
    data_nascimento='1985-05-15',
    cargo=cargo_membro,
    cadastrado_por=admin
)

print('✅ Dados de teste criados com sucesso!')
print(f'👑 Admin: {admin.nome} ({admin.email}) - Senha: admin123')
print(f'👤 Usuario: {usuario.username} ({usuario.email}) - Senha: marketing123')
print(f'🙋 Membro 1: {membro1.nome} ({membro1.email})')
print(f'🙋 Membro 2: {membro2.nome} ({membro2.email})')

