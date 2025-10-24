#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.models import *
from app_alfa.validators import validate_cpf
from django.core.exceptions import ValidationError

def test_cpf_scenarios():
    print("🧪 TESTANDO CENÁRIOS DE CPF")
    print("=" * 50)
    
    # CPFs para testar
    test_cpfs = [
        ("11144477735", "CPF válido conhecido"),
        ("111.444.777-35", "CPF com formatação"),
        ("12345678901", "CPF inválido (que você tentou)"),
        ("11111111111", "CPF com todos iguais"),
        ("123456789", "CPF com poucos dígitos"),
        ("123456789012", "CPF com muitos dígitos"),
    ]
    
    for cpf, descricao in test_cpfs:
        print(f"\n📋 Testando: {cpf} ({descricao})")
        try:
            validate_cpf(cpf)
            print(f"✅ VÁLIDO: {cpf}")
            
            # Verificar se já existe no banco
            if Membro.objects.filter(cpf=cpf).exists():
                print(f"⚠️  JÁ EXISTE no banco!")
            else:
                print(f"✅ Disponível para uso!")
                
        except ValidationError as e:
            print(f"❌ INVÁLIDO: {e}")
    
    print("\n" + "=" * 50)
    print("📊 RESUMO:")
    print("✅ Use CPFs válidos como: 11144477735")
    print("✅ Formato aceito: 111.444.777-35")
    print("❌ Evite: 12345678901 (inválido)")
    print("❌ Evite: CPFs já cadastrados")

if __name__ == "__main__":
    test_cpf_scenarios()

