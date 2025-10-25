"""
Sistema de Relatórios e Analytics - Alfa+
Gera relatórios PDF, Excel e estatísticas do sistema
"""

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import csv
import json
from decimal import Decimal
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io

from .models import Membro, Evento, Transacao, Cargo, EventoPresenca


class RelatorioBase:
    """Classe base para todos os relatórios"""
    
    def __init__(self, data_inicio=None, data_fim=None):
        self.data_inicio = data_inicio or (timezone.now() - timedelta(days=30))
        self.data_fim = data_fim or timezone.now()
    
    def get_context_data(self):
        """Retorna dados comuns para todos os relatórios"""
        return {
            'data_inicio': self.data_inicio,
            'data_fim': self.data_fim,
            'data_geracao': timezone.now(),
        }


class RelatorioMembros(RelatorioBase):
    """Relatório de Membros"""
    
    def get_estatisticas_membros(self):
        """Estatísticas gerais de membros"""
        total_membros = Membro.objects.filter(is_active=True).count()
        membros_ativos = Membro.objects.filter(is_active=True, status='ativo').count()
        membros_inativos = Membro.objects.filter(is_active=True, status='inativo').count()
        
        # Membros por cargo
        membros_por_cargo = Membro.objects.filter(is_active=True).values(
            'cargo__nome'
        ).annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Membros por faixa etária (baseado na data de nascimento)
        membros_por_idade = Membro.objects.filter(
            is_active=True, 
            data_nascimento__isnull=False
        ).extra(
            select={
                'faixa_etaria': """
                CASE 
                    WHEN (julianday('now') - julianday(data_nascimento)) / 365.25 < 18 THEN 'Menor de 18'
                    WHEN (julianday('now') - julianday(data_nascimento)) / 365.25 BETWEEN 18 AND 30 THEN '18-30 anos'
                    WHEN (julianday('now') - julianday(data_nascimento)) / 365.25 BETWEEN 31 AND 50 THEN '31-50 anos'
                    WHEN (julianday('now') - julianday(data_nascimento)) / 365.25 BETWEEN 51 AND 70 THEN '51-70 anos'
                    ELSE 'Acima de 70 anos'
                END
            """
            }
        ).values('faixa_etaria').annotate(total=Count('id'))
        
        return {
            'total_membros': total_membros,
            'membros_ativos': membros_ativos,
            'membros_inativos': membros_inativos,
            'membros_por_cargo': list(membros_por_cargo),
            'membros_por_idade': list(membros_por_idade),
        }
    
    def gerar_pdf(self):
        """Gera relatório PDF de membros usando ReportLab"""
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2563eb')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2563eb')
        )
        
        # Obter dados
        context = self.get_context_data()
        stats = self.get_estatisticas_membros()
        
        # Construir conteúdo
        story = []
        
        # Título
        story.append(Paragraph("🏛️ Sistema Alfa+ - Relatório de Membros", title_style))
        story.append(Spacer(1, 12))
        
        # Período
        story.append(Paragraph(f"<b>Período:</b> {context['data_inicio'].strftime('%d/%m/%Y')} a {context['data_fim'].strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"<b>Gerado em:</b> {context['data_geracao'].strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Estatísticas gerais
        story.append(Paragraph("📊 Estatísticas Gerais", heading_style))
        
        stats_data = [
            ['Total de Membros', str(stats['total_membros'])],
            ['Membros Ativos', str(stats['membros_ativos'])],
            ['Membros Inativos', str(stats['membros_inativos'])],
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # Membros por cargo
        if stats['membros_por_cargo']:
            story.append(Paragraph("👥 Membros por Cargo", heading_style))
            
            cargo_data = [['Cargo', 'Quantidade', 'Percentual']]
            for item in stats['membros_por_cargo']:
                percentual = (item['total'] / stats['total_membros'] * 100) if stats['total_membros'] > 0 else 0
                cargo_data.append([
                    item['cargo__nome'] or 'Sem cargo',
                    str(item['total']),
                    f"{percentual:.1f}%"
                ])
            
            cargo_table = Table(cargo_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            cargo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(cargo_table)
            story.append(Spacer(1, 20))
        
        # Membros por faixa etária
        if stats['membros_por_idade']:
            story.append(Paragraph("📈 Distribuição por Faixa Etária", heading_style))
            
            idade_data = [['Faixa Etária', 'Quantidade', 'Percentual']]
            for item in stats['membros_por_idade']:
                percentual = (item['total'] / stats['total_membros'] * 100) if stats['total_membros'] > 0 else 0
                idade_data.append([
                    item['faixa_etaria'],
                    str(item['total']),
                    f"{percentual:.1f}%"
                ])
            
            idade_table = Table(idade_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            idade_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(idade_table)
            story.append(Spacer(1, 20))
        
        # Lista completa de membros
        story.append(Paragraph("👥 Lista Completa de Membros", heading_style))
        
        # Obter todos os membros ativos
        membros = Membro.objects.filter(is_active=True).order_by('nome')
        
        if membros.exists():
            # Cabeçalho da tabela
            membros_data = [['Nome', 'Email', 'Telefone', 'Cargo', 'Status', 'Data Cadastro']]
            
            for membro in membros:
                # Calcular idade se tiver data de nascimento
                idade_str = ''
                if membro.data_nascimento:
                    from datetime import date
                    hoje = date.today()
                    idade = hoje.year - membro.data_nascimento.year - ((hoje.month, hoje.day) < (membro.data_nascimento.month, membro.data_nascimento.day))
                    idade_str = f" ({idade} anos)"
                
                membros_data.append([
                    f"{membro.nome}{idade_str}",
                    membro.email,
                    membro.telefone or '-',
                    membro.cargo.nome if membro.cargo else 'Sem cargo',
                    membro.status.title(),
                    membro.created_at.strftime('%d/%m/%Y')
                ])
            
            # Criar tabela com quebra de página se necessário
            membros_table = Table(membros_data, colWidths=[2*inch, 2*inch, 1.2*inch, 1.5*inch, 1*inch, 1*inch])
            membros_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            
            story.append(membros_table)
        else:
            story.append(Paragraph("Nenhum membro encontrado no sistema.", styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        # Obter PDF do buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_membros.pdf"'
        return response


class RelatorioFinanceiro(RelatorioBase):
    """Relatório Financeiro"""
    
    def get_estatisticas_financeiras(self):
        """Estatísticas financeiras do período"""
        transacoes = Transacao.objects.filter(
            data__range=[self.data_inicio, self.data_fim]
        )
        
        # Entradas e saídas
        entradas = transacoes.filter(tipo='entrada').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0.00')
        
        saidas = transacoes.filter(tipo='saida').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0.00')
        
        saldo_periodo = entradas - saidas
        
        # Transações por tipo
        transacoes_por_tipo = transacoes.values('tipo').annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        )
        
        # Transações por mês (simplificado - removido por enquanto)
        transacoes_por_mes = []
        
        return {
            'entradas': entradas,
            'saidas': saidas,
            'saldo_periodo': saldo_periodo,
            'transacoes_por_tipo': list(transacoes_por_tipo),
            'transacoes_por_mes': list(transacoes_por_mes),
            'total_transacoes': transacoes.count(),
        }
    
    def gerar_pdf(self):
        """Gera relatório PDF financeiro usando ReportLab"""
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2563eb')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2563eb')
        )
        
        # Obter dados
        context = self.get_context_data()
        stats = self.get_estatisticas_financeiras()
        
        # Construir conteúdo
        story = []
        
        # Título
        story.append(Paragraph("💰 Sistema Alfa+ - Relatório Financeiro", title_style))
        story.append(Spacer(1, 12))
        
        # Período
        story.append(Paragraph(f"<b>Período:</b> {context['data_inicio'].strftime('%d/%m/%Y')} a {context['data_fim'].strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"<b>Gerado em:</b> {context['data_geracao'].strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumo financeiro
        story.append(Paragraph("📊 Resumo Financeiro", heading_style))
        
        finance_data = [
            ['Descrição', 'Valor'],
            ['Total de Entradas', f"R$ {stats['entradas']:.2f}"],
            ['Total de Saídas', f"R$ {stats['saidas']:.2f}"],
            ['Saldo do Período', f"R$ {stats['saldo_periodo']:.2f}"],
            ['Total de Transações', str(stats['total_transacoes'])],
        ]
        
        finance_table = Table(finance_data, colWidths=[3*inch, 2*inch])
        finance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(finance_table)
        story.append(Spacer(1, 20))
        
        # Transações por tipo
        if stats['transacoes_por_tipo']:
            story.append(Paragraph("📈 Transações por Tipo", heading_style))
            
            tipo_data = [['Tipo', 'Quantidade', 'Valor Total']]
            for item in stats['transacoes_por_tipo']:
                tipo_data.append([
                    item['tipo'].title(),
                    str(item['quantidade']),
                    f"R$ {item['total']:.2f}"
                ])
            
            tipo_table = Table(tipo_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            tipo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tipo_table)
            story.append(Spacer(1, 20))
        
        # Lista de transações do período
        story.append(Paragraph("💰 Transações do Período", heading_style))
        
        # Obter transações do período
        transacoes = Transacao.objects.filter(
            data__range=[context['data_inicio'], context['data_fim']]
        ).order_by('-data')
        
        if transacoes.exists():
            # Cabeçalho da tabela
            transacoes_data = [['Data', 'Tipo', 'Valor', 'Descrição', 'Registrado Por']]
            
            for transacao in transacoes:
                transacoes_data.append([
                    transacao.data.strftime('%d/%m/%Y'),
                    transacao.tipo.title(),
                    f"R$ {transacao.valor:.2f}",
                    transacao.descricao[:30] + '...' if len(transacao.descricao) > 30 else transacao.descricao,
                    transacao.registrado_por.nome if transacao.registrado_por else 'Sistema'
                ])
            
            # Criar tabela
            transacoes_table = Table(transacoes_data, colWidths=[1*inch, 1*inch, 1.2*inch, 2*inch, 1.5*inch])
            transacoes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            
            story.append(transacoes_table)
        else:
            story.append(Paragraph("Nenhuma transação encontrada no período.", styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        # Obter PDF do buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.pdf"'
        return response


class RelatorioEventos(RelatorioBase):
    """Relatório de Eventos"""
    
    def get_estatisticas_eventos(self):
        """Estatísticas de eventos"""
        eventos = Evento.objects.filter(
            data__range=[self.data_inicio, self.data_fim]
        )
        
        total_eventos = eventos.count()
        
        # Como não há campo status, vamos usar a data para determinar o status
        from django.utils import timezone
        agora = timezone.now()
        
        eventos_realizados = eventos.filter(data__lt=agora).count()
        eventos_agendados = eventos.filter(data__gte=agora).count()
        eventos_cancelados = 0  # Não há campo para cancelados
        
        # Participação média
        total_participantes = EventoPresenca.objects.filter(
            evento__in=eventos
        ).count()
        participacao_media = (total_participantes / total_eventos * 100) if total_eventos > 0 else 0
        
        # Eventos por tipo (removido pois não há campo tipo)
        eventos_por_tipo = []
        
        # Top 5 eventos com mais participantes
        top_eventos = eventos.annotate(
            total_participantes=Count('presencas')
        ).order_by('-total_participantes')[:5]
        
        return {
            'total_eventos': total_eventos,
            'eventos_realizados': eventos_realizados,
            'eventos_agendados': eventos_agendados,
            'eventos_cancelados': eventos_cancelados,
            'participacao_media': round(participacao_media, 2),
            'eventos_por_tipo': list(eventos_por_tipo),
            'top_eventos': list(top_eventos),
        }
    
    def gerar_pdf(self):
        """Gera relatório PDF de eventos usando ReportLab"""
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2563eb')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2563eb')
        )
        
        # Obter dados
        context = self.get_context_data()
        stats = self.get_estatisticas_eventos()
        
        # Construir conteúdo
        story = []
        
        # Título
        story.append(Paragraph("📅 Sistema Alfa+ - Relatório de Eventos", title_style))
        story.append(Spacer(1, 12))
        
        # Período
        story.append(Paragraph(f"<b>Período:</b> {context['data_inicio'].strftime('%d/%m/%Y')} a {context['data_fim'].strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"<b>Gerado em:</b> {context['data_geracao'].strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Estatísticas de eventos
        story.append(Paragraph("📊 Estatísticas de Eventos", heading_style))
        
        events_data = [
            ['Total de Eventos', str(stats['total_eventos'])],
            ['Eventos Realizados', str(stats['eventos_realizados'])],
            ['Eventos Agendados', str(stats['eventos_agendados'])],
            ['Eventos Cancelados', str(stats['eventos_cancelados'])],
            ['Participação Média', f"{stats['participacao_media']}%"],
        ]
        
        events_table = Table(events_data, colWidths=[3*inch, 2*inch])
        events_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(events_table)
        story.append(Spacer(1, 20))
        
        # Eventos por tipo
        if stats['eventos_por_tipo']:
            story.append(Paragraph("🎯 Eventos por Tipo", heading_style))
            
            tipo_data = [['Tipo de Evento', 'Quantidade', 'Percentual']]
            for item in stats['eventos_por_tipo']:
                percentual = (item['total'] / stats['total_eventos'] * 100) if stats['total_eventos'] > 0 else 0
                tipo_data.append([
                    item['tipo'].title(),
                    str(item['total']),
                    f"{percentual:.1f}%"
                ])
            
            tipo_table = Table(tipo_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            tipo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tipo_table)
            story.append(Spacer(1, 20))
        
        # Top 5 eventos com mais participantes
        if stats['top_eventos']:
            story.append(Paragraph("🏆 Top 5 Eventos com Maior Participação", heading_style))
            
            top_data = [['Evento', 'Data', 'Participantes', 'Status']]
            for evento in stats['top_eventos']:
                # Determinar status baseado na data
                from django.utils import timezone
                agora = timezone.now()
                status = 'Realizado' if evento.data < agora else 'Agendado'
                
                top_data.append([
                    evento.titulo,
                    evento.data.strftime('%d/%m/%Y'),
                    str(evento.total_participantes),
                    status
                ])
            
            top_table = Table(top_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch])
            top_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(top_table)
            story.append(Spacer(1, 20))
        
        # Lista de eventos do período
        story.append(Paragraph("📅 Eventos do Período", heading_style))
        
        # Obter eventos do período
        eventos = Evento.objects.filter(
            data__range=[context['data_inicio'], context['data_fim']]
        ).order_by('-data')
        
        if eventos.exists():
            # Cabeçalho da tabela
            eventos_data = [['Nome', 'Data', 'Local', 'Status', 'Participantes']]
            
            for evento in eventos:
                participantes_count = evento.presencas.count()
                # Determinar status baseado na data
                from django.utils import timezone
                agora = timezone.now()
                status = 'Realizado' if evento.data < agora else 'Agendado'
                
                eventos_data.append([
                    evento.titulo,
                    evento.data.strftime('%d/%m/%Y'),
                    evento.local or '-',
                    status,
                    str(participantes_count)
                ])
            
            # Criar tabela
            eventos_table = Table(eventos_data, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1*inch, 1*inch])
            eventos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            
            story.append(eventos_table)
        else:
            story.append(Paragraph("Nenhum evento encontrado no período.", styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        # Obter PDF do buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_eventos.pdf"'
        return response


class RelatorioGeral(RelatorioBase):
    """Relatório Geral do Sistema"""
    
    def get_dashboard_data(self):
        """Dados para dashboard principal"""
        # Membros
        total_membros = Membro.objects.filter(is_active=True).count()
        membros_ativos = Membro.objects.filter(is_active=True, status='ativo').count()
        
        # Eventos
        total_eventos = Evento.objects.count()
        eventos_este_mes = Evento.objects.filter(
            data__month=timezone.now().month,
            data__year=timezone.now().year
        ).count()
        
        # Financeiro
        entradas_mes = Transacao.objects.filter(
            tipo='entrada',
            data__month=timezone.now().month,
            data__year=timezone.now().year
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        saidas_mes = Transacao.objects.filter(
            tipo='saida',
            data__month=timezone.now().month,
            data__year=timezone.now().year
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        saldo_mes = entradas_mes - saidas_mes
        
        # Crescimento de membros (últimos 6 meses)
        crescimento_membros = []
        for i in range(6):
            data = timezone.now() - timedelta(days=30*i)
            membros_mes = Membro.objects.filter(
                created_at__month=data.month,
                created_at__year=data.year
            ).count()
            crescimento_membros.append({
                'mes': data.strftime('%Y-%m'),
                'membros': membros_mes
            })
        
        return {
            'total_membros': total_membros,
            'membros_ativos': membros_ativos,
            'total_eventos': total_eventos,
            'eventos_este_mes': eventos_este_mes,
            'entradas_mes': float(entradas_mes),
            'saidas_mes': float(saidas_mes),
            'saldo_mes': float(saldo_mes),
            'crescimento_membros': crescimento_membros,
        }


class ExportadorDados:
    """Exportador de dados para Excel/CSV"""
    
    @staticmethod
    def exportar_membros_csv():
        """Exporta membros para CSV"""
        membros = Membro.objects.filter(is_active=True)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="membros.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Nome', 'Email', 'Telefone', 'CPF', 'RG', 'Data Nascimento', 
            'Cargo', 'Status', 'Data Cadastro'
        ])
        
        for membro in membros:
            # Calcular idade baseada na data de nascimento
            idade = ''
            if membro.data_nascimento:
                from datetime import date
                hoje = date.today()
                idade = hoje.year - membro.data_nascimento.year - ((hoje.month, hoje.day) < (membro.data_nascimento.month, membro.data_nascimento.day))
                idade = str(idade)
            
            writer.writerow([
                membro.nome,
                membro.email,
                membro.telefone,
                membro.cpf,
                membro.rg,
                membro.data_nascimento.strftime('%d/%m/%Y') if membro.data_nascimento else '',
                membro.cargo.nome if membro.cargo else '',
                membro.status,
                membro.created_at.strftime('%d/%m/%Y')
            ])
        
        return response
    
    @staticmethod
    def exportar_transacoes_csv():
        """Exporta transações para CSV"""
        transacoes = Transacao.objects.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transacoes.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Data', 'Tipo', 'Valor', 'Descrição', 'Registrado Por'
        ])
        
        for transacao in transacoes:
            writer.writerow([
                transacao.data.strftime('%d/%m/%Y'),
                transacao.tipo,
                transacao.valor,
                transacao.descricao,
                transacao.registrado_por.nome if transacao.registrado_por else ''
            ])
        
        return response
