import os
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alfa_project.settings')
django.setup()

def before_scenario(context, scenario):
    """Limpar o banco de dados antes de cada cenário"""
    from app_Alfa.models import (Admin, Usuario, Evento, FotoEvento, Membro,
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