import os
import sys
import django
import logging
import warnings
from django.conf import settings
from django.test.utils import get_runner, override_settings

# Adicionar o diretório backend ao Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

def before_all(context):
    """Configurar logging antes de todos os testes"""
    # Desabilitar logs de erro do Django durante os testes
    logging.disable(logging.ERROR)
    
    # Suprimir warnings
    warnings.filterwarnings('ignore')
    
    # Configurar Django para não mostrar exceções em requests de teste
    from django.test import override_settings
    context.test_settings = override_settings(
        DEBUG=False,
        LOGGING={
            'version': 1,
            'disable_existing_loggers': True,
            'handlers': {
                'null': {
                    'class': 'logging.NullHandler',
                },
            },
            'loggers': {
                'django.request': {
                    'handlers': ['null'],
                    'level': 'CRITICAL',
                    'propagate': False,
                },
                'django': {
                    'handlers': ['null'],
                    'level': 'CRITICAL',
                    'propagate': False,
                },
            },
        }
    )
    context.test_settings.__enter__()

def after_all(context):
    """Reabilitar logging após todos os testes"""
    if hasattr(context, 'test_settings'):
        context.test_settings.__exit__(None, None, None)
    logging.disable(logging.NOTSET)
    warnings.filterwarnings('default')

def before_scenario(context, scenario):
    """Limpar o banco de dados antes de cada cenário"""
    from app_alfa.models import (Admin, Usuario, Evento, FotoEvento, Membro,
                                  Postagem, FotoPostagem, Cargo, ONG, Oferta, DistribuicaoOferta,
                                  DocumentoMembro, Grupo, Doacao)
    
    # Deletar todos os registros na ordem correta (dependências primeiro)
    Doacao.objects.all().delete()
    DistribuicaoOferta.objects.all().delete()
    DocumentoMembro.objects.all().delete()
    Oferta.objects.all().delete()
    FotoPostagem.objects.all().delete()
    FotoEvento.objects.all().delete()
    Postagem.objects.all().delete()
    Evento.objects.all().delete()
    ONG.objects.all().delete()
    Grupo.objects.all().delete()
    # Deletar usuários antes de deletar cargo (por causa das foreign keys)
    Membro.objects.all().delete()
    Usuario.objects.all().delete()
    Admin.objects.all().delete()
    # Deletar cargo por último
    Cargo.objects.all().delete()