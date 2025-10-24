#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

def test_api_login():
    print('🧪 TESTANDO LOGIN VIA API')
    print('=' * 40)

    # Testar login do admin
    print('\n👑 TESTANDO LOGIN ADMIN:')
    login_data = {
        'email': 'admin@igreja.com',
        'senha': 'admin123'
    }

    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/auth/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print('✅ LOGIN ADMIN: SUCESSO')
                print(f'Token: {data.get("access_token", "")[:20]}...')
            else:
                print(f'❌ LOGIN ADMIN: {data.get("message")}')
        else:
            print(f'❌ ERRO HTTP: {response.status_code}')
            
    except requests.exceptions.ConnectionError:
        print('❌ SERVIDOR NÃO ESTÁ RODANDO')
        print('Execute: python manage.py runserver')
    except Exception as e:
        print(f'❌ ERRO: {e}')

    # Testar login de membro (sem senha)
    print('\n🙋 TESTANDO LOGIN MEMBRO:')
    login_data_membro = {
        'email': 'ana@email.com',
        'senha': 'senha123'
    }

    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/auth/login-membro/',
            json=login_data_membro,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print('✅ LOGIN MEMBRO: SUCESSO')
            else:
                print(f'❌ LOGIN MEMBRO: {data.get("message")}')
        else:
            print(f'❌ ERRO HTTP: {response.status_code}')
            
    except requests.exceptions.ConnectionError:
        print('❌ SERVIDOR NÃO ESTÁ RODANDO')
    except Exception as e:
        print(f'❌ ERRO: {e}')

if __name__ == "__main__":
    test_api_login()

