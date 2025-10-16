from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .models import Transferencia, Membro, Transacao, Evento, Postagem, Usuario, Admin, Comentario
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Crie suas views aqui.
def gerar_pdf_transferencia(request, transferencia_id):
    try:
        transferencia = Transferencia.objects.get(id=transferencia_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título
        title = Paragraph("Documento de Transferência de Membro", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))

        # Dados
        story.append(Paragraph(f"Membro: {transferencia.membro.nome}", styles['Normal']))
        story.append(Paragraph(f"Igreja Origem: {transferencia.igreja_origem.nome}", styles['Normal']))
        story.append(Paragraph(f"Igreja Destino: {transferencia.igreja_destino.nome}", styles['Normal']))
        story.append(Paragraph(f"Data: {transferencia.data_transferencia}", styles['Normal']))
        story.append(Paragraph(f"Motivo: {transferencia.motivo}", styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="transferencia_{transferencia_id}.pdf"'
        return response
    except Transferencia.DoesNotExist:
        return HttpResponse('Transferência não encontrada', status=404)

def gerar_cartao_membro(request, membro_id):
    try:
        membro = Membro.objects.get(id=membro_id)
        html_string = render_to_string('cartao_membro_template.html', {'membro': membro})
        pdf = weasyprint.HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="cartao_membro_{membro_id}.pdf"'
        return response
    except Membro.DoesNotExist:
        return HttpResponse('Membro não encontrado', status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transacao_create(request):
    try:
        data = request.data

        # Usar o usuário autenticado via JWT
        user = request.user
        admin_user = Admin.objects.filter(user_ptr=user).first()
        if not admin_user or not admin_user.cargo:
            return JsonResponse({
                'success': False,
                'message': 'Admin sem cargo definido ou permissões insuficientes'
            }, status=403)

        # Verificar se o tipo de transação requer permissão específica
        tipo = data['tipo']
        if tipo == 'entrada' and data['categoria'].lower() in ['dízimo', 'dizimo']:
            if not admin_user.cargo.pode_registrar_dizimos:
                return JsonResponse({
                    'success': False,
                    'message': 'Permissões insuficientes para registrar dízimos'
                }, status=403)
        elif tipo == 'entrada' and data['categoria'].lower() == 'oferta':
            if not admin_user.cargo.pode_registrar_ofertas:
                return JsonResponse({
                    'success': False,
                    'message': 'Permissões insuficientes para registrar ofertas'
                }, status=403)

        transacao = Transacao.objects.create(
            tipo=data['tipo'],
            categoria=data['categoria'],
            valor=data['valor'],
            data=data['data'],
            descricao=data['descricao'],
            metodo_pagamento=data.get('metodoPagamento'),
            observacoes=data.get('observacoes'),
            registrado_por=admin_user
        )
        return JsonResponse({
            'success': True,
            'message': 'Transação registrada com sucesso!',
            'transacao_id': transacao.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao registrar transação: {str(e)}'
        }, status=400)

@csrf_exempt
def evento_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Criar usuário padrão se não existir
            organizador, created = Usuario.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@igreja.com',
                    'is_active': True,
                    'is_staff': True
                }
            )

            from datetime import datetime
            data_str = data['data'] + ' ' + data.get('hora', '00:00')
            data_datetime = datetime.strptime(data_str, '%Y-%m-%d %H:%M')

            evento = Evento.objects.create(
                titulo=data['titulo'],
                descricao=data['descricao'],
                data=data_datetime,
                local=data.get('local'),
                organizador=organizador
            )
            return JsonResponse({
                'success': True,
                'message': 'Evento criado com sucesso!',
                'evento_id': evento.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao criar evento: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    }, status=405)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postagem_create(request):
    try:
        data = request.data

        # Usar o usuário autenticado via JWT
        user = request.user
        admin_user = Admin.objects.filter(user_ptr=user).first()
        if not admin_user or not admin_user.cargo:
            return JsonResponse({
                'success': False,
                'message': 'Admin sem cargo definido ou permissões insuficientes'
            }, status=403)

        # Verificar permissões para fazer postagens
        if not admin_user.cargo.pode_fazer_postagens:
            return JsonResponse({
                'success': False,
                'message': 'Permissões insuficientes para criar postagens'
            }, status=403)

        postagem = Postagem.objects.create(
            titulo=data['titulo'],
            conteudo=data['conteudo'],
            autor=admin_user
        )
        return JsonResponse({
            'success': True,
            'message': 'Postagem criada com sucesso!',
            'postagem_id': postagem.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao criar postagem: {str(e)}'
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comentario_create(request):
    try:
        data = request.data

        # Usar o usuário autenticado via JWT
        user = request.user
        usuario = Usuario.objects.filter(id=user.id).first()
        if not usuario:
            return JsonResponse({
                'success': False,
                'message': 'Usuário não encontrado'
            }, status=404)

        # Verificar se evento ou postagem foi fornecido
        evento_id = data.get('evento_id')
        postagem_id = data.get('postagem_id')

        if not evento_id and not postagem_id:
            return JsonResponse({
                'success': False,
                'message': 'Deve fornecer evento_id ou postagem_id'
            }, status=400)

        if evento_id and postagem_id:
            return JsonResponse({
                'success': False,
                'message': 'Não pode comentar em evento e postagem ao mesmo tempo'
            }, status=400)

        # Verificar se o evento ou postagem existe
        if evento_id:
            try:
                Evento.objects.get(id=evento_id)
            except Evento.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Evento não encontrado'
                }, status=404)
        elif postagem_id:
            try:
                Postagem.objects.get(id=postagem_id)
            except Postagem.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Postagem não encontrada'
                }, status=404)

        comentario = Comentario.objects.create(
            evento_id=evento_id if evento_id else None,
            postagem_id=postagem_id if postagem_id else None,
            autor=usuario,
            conteudo=data['conteudo']
        )
        return JsonResponse({
            'success': True,
            'message': 'Comentário criado com sucesso!',
            'comentario_id': comentario.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao criar comentário: {str(e)}'
        }, status=400)
