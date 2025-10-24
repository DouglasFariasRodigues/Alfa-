#!/usr/bin/env python
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from app_alfa.serializers import MembroCreateSerializer
from django.core.exceptions import ValidationError

def test_member_creation():
    print('🧪 TESTANDO CRIAÇÃO DE MEMBROS')
    print('=' * 50)

    # Dados de teste para membro
    test_data = {
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'telefone': '11999999999',
        'cpf': '12345678909',  # CPF válido
        'rg': '123456789',
        'data_nascimento': '1990-01-01',
        'endereco': 'Rua Teste, 123',
        'senha': 'joao123',
        'status': 'ativo',
        'cargo': 1  # ID do cargo
    }

    print('\n📋 DADOS DE TESTE:')
    for key, value in test_data.items():
        print(f'  {key}: {value}')

    print('\n🔍 TESTANDO VALIDAÇÕES:')
    
    # Testar validação de CPF
    try:
        from app_alfa.validators import validate_cpf
        validate_cpf(test_data['cpf'])
        print('✅ CPF: VÁLIDO')
    except ValidationError as e:
        print(f'❌ CPF: {e}')

    # Testar validação de telefone
    try:
        from app_alfa.validators import validate_phone
        validate_phone(test_data['telefone'])
        print('✅ Telefone: VÁLIDO')
    except ValidationError as e:
        print(f'❌ Telefone: {e}')

    # Testar validação de senha
    try:
        from app_alfa.models import validate_password_strength
        validate_password_strength(test_data['senha'])
        print('✅ Senha: VÁLIDA')
    except ValidationError as e:
        print(f'❌ Senha: {e}')

    # Testar validação de idade
    try:
        from app_alfa.validators import validate_age
        from datetime import datetime
        data_nasc = datetime.strptime(test_data['data_nascimento'], '%Y-%m-%d').date()
        validate_age(data_nasc)
        print('✅ Data nascimento: VÁLIDA')
    except ValidationError as e:
        print(f'❌ Data nascimento: {e}')

    print('\n🧪 TESTANDO SERIALIZER:')
    try:
        serializer = MembroCreateSerializer(data=test_data)
        if serializer.is_valid():
            print('✅ Serializer: VÁLIDO')
            print('Dados validados:', serializer.validated_data)
        else:
            print('❌ Serializer: INVÁLIDO')
            print('Erros:', serializer.errors)
    except Exception as e:
        print(f'❌ Erro no serializer: {e}')

    print('\n🧪 TESTANDO CRIAÇÃO DIRETA:')
    try:
        # Pegar admin e cargo
        admin = Admin.objects.first()
        cargo = Cargo.objects.first()
        
        if not admin:
            print('❌ Nenhum admin encontrado')
            return
            
        if not cargo:
            print('❌ Nenhum cargo encontrado')
            return

        # Criar membro diretamente
        membro = Membro.objects.create(
            nome=test_data['nome'],
            email=test_data['email'],
            telefone=test_data['telefone'],
            cpf=test_data['cpf'],
            rg=test_data['rg'],
            data_nascimento=test_data['data_nascimento'],
            endereco=test_data['endereco'],
            senha=test_data['senha'],
            status=test_data['status'],
            cargo=cargo,
            cadastrado_por=admin
        )
        print('✅ Membro criado com sucesso!')
        print(f'ID: {membro.id}, Nome: {membro.nome}')
        
        # Limpar teste
        membro.delete()
        print('✅ Membro de teste removido')
        
    except Exception as e:
        print(f'❌ Erro ao criar membro: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_member_creation()

