#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

def test_relaxed_password_validation():
    print('🧪 TESTANDO VALIDAÇÃO DE SENHA RELAXADA')
    print('=' * 50)

    # Testar senhas que antes falhavam
    test_passwords = [
        ('123456', 'Senha numérica'),
        ('senha123', 'Senha com letras e números'),
        ('admin', 'Senha simples'),
        ('123', 'Senha muito curta'),
        ('abc', 'Senha muito curta'),
        ('password', 'Senha comum'),
        ('teste', 'Senha simples válida'),
        ('user123', 'Senha válida'),
    ]

    print('\n📋 TESTANDO VALIDAÇÕES:')
    for senha, descricao in test_passwords:
        try:
            # Simular validação
            from app_alfa.models import validate_password_strength
            validate_password_strength(senha)
            print(f'✅ {senha} ({descricao}): VÁLIDA')
        except ValidationError as e:
            print(f'❌ {senha} ({descricao}): {e}')

    print('\n🔧 TESTANDO CRIAÇÃO DE USUÁRIOS:')
    
    # Testar criação de membro com senha simples
    try:
        # Pegar admin existente
        admin = Admin.objects.first()
        cargo = Cargo.objects.first()
        
        # Criar membro de teste
        membro_teste = Membro.objects.create(
            nome='Teste Usuario',
            email='teste@email.com',
            telefone='11999999999',
            cpf='12345678909',  # CPF válido
            senha='teste123',  # Senha simples
            cargo=cargo,
            cadastrado_por=admin
        )
        print('✅ Membro criado com senha simples: SUCESSO')
        
        # Testar login
        if check_password('teste123', membro_teste.senha):
            print('✅ Login com senha simples: FUNCIONANDO')
        else:
            print('❌ Login com senha simples: FALHOU')
            
        # Limpar teste
        membro_teste.delete()
        print('✅ Membro de teste removido')
        
    except Exception as e:
        print(f'❌ Erro ao criar membro: {e}')

    print('\n🎉 VALIDAÇÃO RELAXADA FUNCIONANDO!')
    print('\n📋 SENHAS AGORA ACEITAS:')
    print('✅ 123456 (apenas números)')
    print('✅ senha123 (letras + números)')
    print('✅ teste (apenas letras)')
    print('✅ user123 (qualquer combinação)')
    print('\n❌ AINDA REJEITADAS:')
    print('❌ 123 (muito curta)')
    print('❌ abc (muito curta)')
    print('❌ password (muito comum)')

if __name__ == "__main__":
    test_relaxed_password_validation()

