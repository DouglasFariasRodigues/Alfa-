#!/usr/bin/env python
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from app_alfa.models import Admin

def test_api_member_creation():
    print('🧪 TESTANDO API DE CRIAÇÃO DE MEMBROS')
    print('=' * 50)

    # Criar cliente de teste
    client = Client()
    
    # Dados de teste
    member_data = {
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'telefone': '11999999999',
        'cpf': '12345678909',
        'rg': '123456789',
        'data_nascimento': '1990-01-01',
        'endereco': 'Rua Teste, 123',
        'senha': 'joao123',
        'status': 'ativo',
        'cargo': 1
    }

    print('\n📋 DADOS ENVIADOS:')
    for key, value in member_data.items():
        print(f'  {key}: {value}')

    # Simular autenticação (criar usuário JWT)
    try:
        # Criar usuário Django para JWT
        user, created = User.objects.get_or_create(
            username='admin@igreja.com',
            defaults={'email': 'admin@igreja.com', 'is_staff': True}
        )
        
        # Fazer login
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        print(f'\n🔑 Token gerado: {access_token[:20]}...')
        
        # Fazer requisição para criar membro
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = client.post(
            '/api/membros/',
            data=json.dumps(member_data),
            content_type='application/json',
            **headers
        )
        
        print(f'\n📊 RESPOSTA DA API:')
        print(f'Status Code: {response.status_code}')
        print(f'Content: {response.content.decode()}')
        
        if response.status_code == 201:
            print('✅ MEMBRO CRIADO COM SUCESSO!')
        elif response.status_code == 400:
            print('❌ ERRO 400 - DADOS INVÁLIDOS:')
            try:
                error_data = json.loads(response.content)
                print('Erros detalhados:')
                for field, errors in error_data.items():
                    print(f'  {field}: {errors}')
            except:
                print('Erro não é JSON válido')
        else:
            print(f'❌ ERRO {response.status_code}')
            
    except Exception as e:
        print(f'❌ ERRO GERAL: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_member_creation()

