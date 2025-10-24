"""
Validadores customizados para o sistema Alfa+
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cpf(value):
    """
    Valida CPF brasileiro
    """
    if not value:
        return
    
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', value)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        raise ValidationError(_('CPF deve ter 11 dígitos.'))
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        raise ValidationError(_('CPF inválido.'))
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        raise ValidationError(_('CPF inválido.'))
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        raise ValidationError(_('CPF inválido.'))


def validate_phone(value):
    """
    Valida telefone brasileiro
    """
    if not value:
        return
    
    # Remove caracteres não numéricos
    phone = re.sub(r'[^0-9]', '', value)
    
    # Verifica se tem 10 ou 11 dígitos
    if len(phone) not in [10, 11]:
        raise ValidationError(_('Telefone deve ter 10 ou 11 dígitos.'))
    
    # Verifica se começa com DDD válido (11-99)
    ddd = int(phone[:2])
    if ddd < 11 or ddd > 99:
        raise ValidationError(_('DDD inválido.'))


def validate_email_domain(value):
    """
    Valida domínio de email (opcional - pode ser usado para restringir domínios)
    """
    if not value:
        return
    
    # Lista de domínios permitidos (mais flexível)
    allowed_domains = [
        'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com',
        'igreja.com', 'igreja.org', 'igreja.net', 'email.com',
        'teste.com', 'exemplo.com', 'alfa.com'
    ]
    
    domain = value.split('@')[1].lower()
    if domain not in allowed_domains:
        raise ValidationError(_(f'Domínio de email não permitido. Domínios aceitos: {", ".join(allowed_domains)}'))


def validate_rg(value):
    """
    Valida RG brasileiro
    """
    if not value:
        return
    
    # Remove caracteres não alfanuméricos
    rg = re.sub(r'[^0-9A-Za-z]', '', value.upper())
    
    # Verifica se tem pelo menos 7 caracteres
    if len(rg) < 7:
        raise ValidationError(_('RG deve ter pelo menos 7 caracteres.'))
    
    # Verifica se tem no máximo 12 caracteres
    if len(rg) > 12:
        raise ValidationError(_('RG deve ter no máximo 12 caracteres.'))


def validate_cep(value):
    """
    Valida CEP brasileiro
    """
    if not value:
        return
    
    # Remove caracteres não numéricos
    cep = re.sub(r'[^0-9]', '', value)
    
    # Verifica se tem 8 dígitos
    if len(cep) != 8:
        raise ValidationError(_('CEP deve ter 8 dígitos.'))
    
    # Verifica se não é sequência de números iguais
    if cep == cep[0] * 8:
        raise ValidationError(_('CEP inválido.'))


def validate_age(value):
    """
    Valida idade mínima (18 anos)
    """
    if not value:
        return
    
    from datetime import date
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 18:
        raise ValidationError(_('Idade mínima de 18 anos.'))
    
    if age > 120:
        raise ValidationError(_('Idade inválida.'))
