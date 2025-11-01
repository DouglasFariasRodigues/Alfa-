"""
Steps para visualização de fotos de eventos pelo Admin.
Testa se o Admin consegue ver fotos dos eventos e cultos realizados na igreja.
"""
from behave import given, when, then
from app_alfa.models import Admin, Usuario, Evento, FotoEvento
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.utils import timezone

# Passo: Criar Admin logado no sistema
@given('que existe um Admin logado')
def step_given_admin_logged(context):
    # Cria Admin com permissões de staff
    context.admin = Admin.objects.create(
        nome="Admin Test",
        email="admin@test.com",
        senha="password123",
        is_active=True,
        is_staff=True
    )
    
    # Criar usuário organizador para os eventos
    context.usuario = Usuario.objects.create(
        username="organizador",
        email="organizador@test.com",
        senha="password123"
    )

# Passo: Criar evento com fotos
@given('existe um evento "{titulo}" com {quantidade:d} fotos')
def step_given_event_with_photos(context, titulo, quantidade):
    # Criar organizador se não existir
    if not hasattr(context, 'usuario'):
        context.usuario = Usuario.objects.create(
            username="organizador",
            email="organizador@test.com",
            senha="password123"
        )
    
    # Criar evento (culto, missa, encontro, etc.)
    evento = Evento.objects.create(
        titulo=titulo,
        descricao=f"Descrição do {titulo}",
        data=timezone.now(),
        local="Igreja Central",
        organizador=context.usuario
    )
    
    # Criar múltiplas fotos para o evento
    for i in range(quantidade):
        FotoEvento.objects.create(
            evento=evento,
            descricao=f"Foto {i+1} do {titulo}",
            imagem=f"eventos_fotos/foto_{i+1}.jpg"
        )
    
    context.evento = evento  # Para compatibilidade com outros steps

# Passo: Criar evento sem fotos
@given('existe um evento "{titulo}" sem fotos')
def step_given_event_without_photos(context, titulo):
    # Criar evento mas não adicionar fotos
    Evento.objects.create(
        titulo=titulo,
        descricao=f"Descrição do {titulo}",
        data=timezone.now(),
        local="Igreja Central",
        organizador=context.usuario
    )

# Passo: Admin solicita ver fotos de um evento específico
@when('o Admin solicita visualizar as fotos do evento "{titulo}"')
def step_when_view_event_photos(context, titulo):
    try:
        # Busca evento pelo título
        evento = Evento.objects.get(titulo=titulo)
        context.evento_atual = evento
        # Lista todas as fotos do evento
        context.fotos = list(evento.fotos.all())
    except Evento.DoesNotExist:
        # Evento não existe
        context.evento_atual = None
        context.fotos = []

# Passo: Admin solicita ver todos eventos que têm fotos
@when('o Admin solicita visualizar todos os eventos com fotos')
def step_when_view_all_events_with_photos(context):
    context.eventos_com_fotos = []
    # Percorre todos os eventos
    for evento in Evento.objects.all():
        if evento.fotos.exists():
            # Adiciona evento com contagem de fotos
            context.eventos_com_fotos.append({
                'evento': evento,
                'quantidade_fotos': evento.fotos.count()
            })

# Passo: Verificar quantidade de fotos visualizadas
@then('o Admin deve ver {quantidade:d} fotos do evento')
def step_then_see_photos(context, quantidade):
    # Compara quantidade esperada com quantidade real
    assert len(context.fotos) == quantidade, \
        f"Esperado {quantidade} fotos, mas encontrou {len(context.fotos)}"

# Passo: Verificar mensagem de evento sem fotos
@then('o Admin deve ver uma mensagem indicando que não há fotos')
def step_then_no_photos_message(context):
    # Confirma que lista de fotos está vazia
    assert len(context.fotos) == 0, \
        f"Evento deveria não ter fotos, mas tem {len(context.fotos)}"

# Passo: Verificar quantidade de eventos listados
@then('o Admin deve ver {quantidade:d} eventos listados')
def step_then_see_events_listed(context, quantidade):
    # Compara quantidade esperada de eventos com fotos
    assert len(context.eventos_com_fotos) == quantidade, \
        f"Esperado {quantidade} eventos, mas encontrou {len(context.eventos_com_fotos)}"

# Passo: Verificar se evento específico tem quantidade correta de fotos
@then('o evento "{titulo}" deve ter {quantidade:d} fotos')
def step_then_event_has_photos(context, titulo, quantidade):
    # Se lista de eventos existe, buscar nela
    if hasattr(context, 'eventos_com_fotos'):
        evento_info = next((e for e in context.eventos_com_fotos if e['evento'].titulo == titulo), None)
        assert evento_info is not None, f"Evento '{titulo}' não encontrado"
        assert evento_info['quantidade_fotos'] == quantidade, \
            f"Evento '{titulo}' deveria ter {quantidade} fotos, mas tem {evento_info['quantidade_fotos']}"
    else:
        # Caso contrário, buscar diretamente do banco
        evento = Evento.objects.get(titulo=titulo)
        count = evento.fotos.count()
        assert count == quantidade, f"Evento '{titulo}' deveria ter {quantidade} fotos, mas tem {count}"
