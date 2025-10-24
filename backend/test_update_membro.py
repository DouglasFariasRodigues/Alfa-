#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import Membro, Admin
from django.contrib.auth.hashers import make_password

def test_update_membro():
    print('🧪 TESTANDO ATUALIZAÇÃO DE MEMBRO')
    print('=' * 40)
    
    # Verificar se há membros existentes
    membros = Membro.objects.all()
    print(f'📋 MEMBROS EXISTENTES: {membros.count()}')
    
    if membros.exists():
        membro = membros.first()
        print(f'✅ Membro encontrado: {membro.nome} (ID: {membro.id})')
        
        # Dados para atualização
        update_data = {
            'nome': f'{membro.nome} (Atualizado)',
            'telefone': '(11) 99999-9999',
            'endereco': 'Endereço atualizado',
            'observacoes': 'Observações atualizadas'
        }
        
        print(f'📝 Dados para atualização: {update_data}')
        
        # Testar atualização via API
        try:
            # Primeiro, fazer login como admin
            login_data = {
                'email': 'admin@igreja.com',
                'senha': 'admin123'
            }
            
            login_response = requests.post('http://127.0.0.1:8000/api/auth/login_admin/', json=login_data)
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                token = login_result.get('access')
                
                if token:
                    print('✅ Login realizado com sucesso')
                    
                    # Fazer requisição de atualização
                    headers = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                    
                    update_response = requests.patch(
                        f'http://127.0.0.1:8000/api/membros/{membro.id}/',
                        json=update_data,
                        headers=headers
                    )
                    
                    print(f'📊 Status Code: {update_response.status_code}')
                    print(f'📋 Response: {update_response.text}')
                    
                    if update_response.status_code == 200:
                        print('✅ Atualização funcionou!')
                        
                        # Verificar se os dados foram atualizados no banco
                        membro.refresh_from_db()
                        print(f'✅ Nome atualizado: {membro.nome}')
                        print(f'✅ Telefone atualizado: {membro.telefone}')
                        print(f'✅ Endereço atualizado: {membro.endereco}')
                    else:
                        print('❌ Atualização falhou!')
                        print(f'Erro: {update_response.text}')
                else:
                    print('❌ Token não encontrado na resposta de login')
            else:
                print('❌ Login falhou!')
                print(f'Status: {login_response.status_code}')
                print(f'Response: {login_response.text}')
                
        except requests.exceptions.ConnectionError:
            print('❌ Servidor não está rodando!')
            print('💡 Execute: python manage.py runserver')
        except Exception as e:
            print(f'❌ Erro: {e}')
            import traceback
            traceback.print_exc()
    else:
        print('❌ Nenhum membro encontrado!')
        print('💡 Crie um membro primeiro no Django Admin')

if __name__ == "__main__":
    test_update_membro()
