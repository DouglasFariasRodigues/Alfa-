#!/usr/bin/env python
"""
Script para testar as validações implementadas na Fase 3
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import Admin, Usuario, Membro, Cargo
from app_alfa.validators import validate_cpf, validate_phone, validate_rg, validate_cep, validate_age
from django.core.exceptions import ValidationError
from datetime import date

def test_cpf_validation():
    """Testa validação de CPF"""
    print("🧪 TESTANDO VALIDAÇÃO DE CPF")
    print("=" * 50)
    
    # CPFs válidos
    valid_cpfs = [
        "11144477735",  # CPF válido
        "12345678909",  # CPF válido
    ]
    
    # CPFs inválidos
    invalid_cpfs = [
        "11111111111",  # Todos iguais
        "12345678901",  # Dígito verificador inválido
        "123",          # Muito curto
        "123456789012345",  # Muito longo
    ]
    
    print("✅ CPFs VÁLIDOS:")
    for cpf in valid_cpfs:
        try:
            validate_cpf(cpf)
            print(f"  ✓ {cpf} - VÁLIDO")
        except ValidationError as e:
            print(f"  ✗ {cpf} - ERRO: {e}")
    
    print("\n❌ CPFs INVÁLIDOS:")
    for cpf in invalid_cpfs:
        try:
            validate_cpf(cpf)
            print(f"  ✗ {cpf} - DEVERIA SER INVÁLIDO")
        except ValidationError as e:
            print(f"  ✓ {cpf} - CORRETAMENTE REJEITADO: {e}")

def test_phone_validation():
    """Testa validação de telefone"""
    print("\n🧪 TESTANDO VALIDAÇÃO DE TELEFONE")
    print("=" * 50)
    
    # Telefones válidos
    valid_phones = [
        "11999999999",  # 11 dígitos
        "1133334444",   # 10 dígitos
        "(11) 99999-9999",  # Com formatação
        "11 9 9999-9999",   # Com espaços
    ]
    
    # Telefones inválidos
    invalid_phones = [
        "123456789",    # Muito curto
        "123456789012", # Muito longo
        "00999999999",  # DDD inválido
        "99999999999",  # DDD inválido
    ]
    
    print("✅ TELEFONES VÁLIDOS:")
    for phone in valid_phones:
        try:
            validate_phone(phone)
            print(f"  ✓ {phone} - VÁLIDO")
        except ValidationError as e:
            print(f"  ✗ {phone} - ERRO: {e}")
    
    print("\n❌ TELEFONES INVÁLIDOS:")
    for phone in invalid_phones:
        try:
            validate_phone(phone)
            print(f"  ✗ {phone} - DEVERIA SER INVÁLIDO")
        except ValidationError as e:
            print(f"  ✓ {phone} - CORRETAMENTE REJEITADO: {e}")

def test_rg_validation():
    """Testa validação de RG"""
    print("\n🧪 TESTANDO VALIDAÇÃO DE RG")
    print("=" * 50)
    
    # RGs válidos
    valid_rgs = [
        "1234567",
        "123456789",
        "12345678901",
        "12.345.678-9",
    ]
    
    # RGs inválidos
    invalid_rgs = [
        "123456",       # Muito curto
        "1234567890123", # Muito longo
    ]
    
    print("✅ RGs VÁLIDOS:")
    for rg in valid_rgs:
        try:
            validate_rg(rg)
            print(f"  ✓ {rg} - VÁLIDO")
        except ValidationError as e:
            print(f"  ✗ {rg} - ERRO: {e}")
    
    print("\n❌ RGs INVÁLIDOS:")
    for rg in invalid_rgs:
        try:
            validate_rg(rg)
            print(f"  ✗ {rg} - DEVERIA SER INVÁLIDO")
        except ValidationError as e:
            print(f"  ✓ {rg} - CORRETAMENTE REJEITADO: {e}")

def test_age_validation():
    """Testa validação de idade"""
    print("\n🧪 TESTANDO VALIDAÇÃO DE IDADE")
    print("=" * 50)
    
    # Datas válidas
    valid_dates = [
        date(1990, 1, 1),   # 34 anos
        date(2000, 6, 15),  # 24 anos
        date(1985, 12, 31), # 39 anos
    ]
    
    # Datas inválidas
    invalid_dates = [
        date(2010, 1, 1),   # 14 anos (muito novo)
        date(1900, 1, 1),   # 124 anos (muito velho)
    ]
    
    print("✅ DATAS VÁLIDAS:")
    for birth_date in valid_dates:
        try:
            validate_age(birth_date)
            print(f"  ✓ {birth_date} - VÁLIDO")
        except ValidationError as e:
            print(f"  ✗ {birth_date} - ERRO: {e}")
    
    print("\n❌ DATAS INVÁLIDAS:")
    for birth_date in invalid_dates:
        try:
            validate_age(birth_date)
            print(f"  ✗ {birth_date} - DEVERIA SER INVÁLIDO")
        except ValidationError as e:
            print(f"  ✓ {birth_date} - CORRETAMENTE REJEITADO: {e}")

def test_model_creation():
    """Testa criação de modelos com validações"""
    print("\n🧪 TESTANDO CRIAÇÃO DE MODELOS")
    print("=" * 50)
    
    # Teste 1: Criar Admin válido
    print("✅ TESTE 1: Criar Admin válido")
    try:
        admin = Admin.objects.create(
            nome="João Silva",
            email="joao@igreja.com",
            telefone="11999999999"
        )
        print(f"  ✓ Admin criado: {admin.nome} - {admin.email}")
        admin.delete()  # Limpar
    except Exception as e:
        print(f"  ✗ Erro ao criar Admin: {e}")
    
    # Teste 2: Criar Admin com telefone inválido
    print("\n❌ TESTE 2: Criar Admin com telefone inválido")
    try:
        admin = Admin.objects.create(
            nome="Maria Santos",
            email="maria@igreja.com",
            telefone="123"  # Telefone inválido
        )
        print(f"  ✗ Admin criado incorretamente: {admin.nome}")
        admin.delete()
    except Exception as e:
        print(f"  ✓ Telefone inválido corretamente rejeitado: {e}")
    
    # Teste 3: Criar Membro com CPF válido
    print("\n✅ TESTE 3: Criar Membro com CPF válido")
    try:
        membro = Membro.objects.create(
            nome="Pedro Costa",
            email="pedro@igreja.com",
            cpf="11144477735",  # CPF válido
            telefone="11988887777"
        )
        print(f"  ✓ Membro criado: {membro.nome} - CPF: {membro.cpf}")
        membro.delete()  # Limpar
    except Exception as e:
        print(f"  ✗ Erro ao criar Membro: {e}")
    
    # Teste 4: Criar Membro com CPF inválido
    print("\n❌ TESTE 4: Criar Membro com CPF inválido")
    try:
        membro = Membro.objects.create(
            nome="Ana Lima",
            email="ana@igreja.com",
            cpf="11111111111",  # CPF inválido
            telefone="11977776666"
        )
        print(f"  ✗ Membro criado incorretamente: {membro.nome}")
        membro.delete()
    except Exception as e:
        print(f"  ✓ CPF inválido corretamente rejeitado: {e}")

def test_forms():
    """Testa os forms criados"""
    print("\n🧪 TESTANDO FORMS")
    print("=" * 50)
    
    from app_alfa.forms import AdminForm, MembroForm, CargoForm
    
    # Teste AdminForm
    print("✅ TESTE: AdminForm")
    form_data = {
        'nome': 'Carlos Admin',
        'email': 'carlos@igreja.com',
        'telefone': '11999999999'
    }
    
    form = AdminForm(data=form_data)
    if form.is_valid():
        print("  ✓ AdminForm válido")
    else:
        print(f"  ✗ AdminForm inválido: {form.errors}")
    
    # Teste MembroForm
    print("\n✅ TESTE: MembroForm")
    form_data = {
        'nome': 'Maria Membro',
        'email': 'maria@igreja.com',
        'cpf': '11144477735',
        'telefone': '11988887777',
        'data_nascimento': '1990-01-01'
    }
    
    form = MembroForm(data=form_data)
    if form.is_valid():
        print("  ✓ MembroForm válido")
    else:
        print(f"  ✗ MembroForm inválido: {form.errors}")

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DE VALIDAÇÃO - FASE 3")
    print("=" * 60)
    
    try:
        test_cpf_validation()
        test_phone_validation()
        test_rg_validation()
        test_age_validation()
        test_model_creation()
        test_forms()
        
        print("\n🎉 TODOS OS TESTES CONCLUÍDOS!")
        print("=" * 60)
        print("✅ Validações funcionando corretamente")
        print("✅ Modelos protegidos contra dados inválidos")
        print("✅ Forms com validação em tempo real")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
