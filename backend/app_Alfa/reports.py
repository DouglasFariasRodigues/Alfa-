"""
Sistema de Relatórios e Analytics - Alfa+ (VERSÃO MELHORADA)
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io

from .models import Membro, Evento, Transacao, Cargo, EventoPresenca
from .pdf_templates import PDFStyles, PDFHeader, PDFFooter, PDFCharts, PDFMetrics, PDFTable
from .pdf_utils import MetricsCalculator


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
    """Relatório de Membros com design profissional"""
    
    def __init__(self, data_inicio=None, data_fim=None):
        super().__init__(data_inicio, data_fim)
        self.styles = PDFStyles()
        self.header = PDFHeader(self.styles)
        self.footer = PDFFooter(self.styles)
        self.charts = PDFCharts(self.styles)
        self.metrics = PDFMetrics(self.styles)
        self.table = PDFTable(self.styles)
        self.calculator = MetricsCalculator(data_inicio, data_fim)
    
    def get_estatisticas_membros(self):
        """Estatísticas gerais de membros usando o novo sistema"""
        return self.calculator.calculate_member_metrics()
    
    def gerar_pdf(self):
        """Gera relatório PDF de membros com design profissional"""
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Obter métricas
        metrics = self.get_estatisticas_membros()
        
        # Construir conteúdo do PDF
        story = []
        
        # 1. Cabeçalho
        titulo = "📊 RELATÓRIO DE MEMBROS"
        subtitulo = f"Período: {self.calculator.get_period_description()}"
        story.extend(self.header.create_header(titulo, subtitulo, timezone.now()))
        
        # 2. Resumo Executivo
        resumo_metrics = [
            {
                'label': 'Total de Membros',
                'value': str(metrics['total_membros']),
                'change': ''
            },
            {
                'label': 'Membros Ativos',
                'value': f"{metrics['membros_ativos']} ({metrics['taxa_ativos']:.1f}%)",
                'change': ''
            },
            {
                'label': 'Novos Este Mês',
                'value': str(metrics['novos_este_mes']),
                'change': f"{metrics['crescimento']:+.1f}%" if metrics['crescimento'] != 0 else ''
            }
        ]
        story.extend(self.metrics.create_metrics_summary(resumo_metrics))
        
        # 3. Gráfico de Status
        if metrics['status_distribution']:
            story.append(Paragraph("📈 DISTRIBUIÇÃO POR STATUS", self.styles['CabecSecao']))
            chart = self.charts.create_pie_chart(
                metrics['status_distribution'],
                "Status dos Membros",
                width=4*inch,
                height=3*inch
            )
            story.append(chart)
            story.append(Spacer(1, 0.2*inch))
        
        # 4. Gráfico de Faixa Etária
        if metrics['faixas_etarias'] and any(metrics['faixas_etarias'].values()):
            story.append(Paragraph("👥 DISTRIBUIÇÃO POR FAIXA ETÁRIA", self.styles['CabecSecao']))
            chart = self.charts.create_bar_chart(
                metrics['faixas_etarias'],
                "Faixas Etárias",
                width=6*inch,
                height=3*inch
            )
            story.append(chart)
            story.append(Spacer(1, 0.2*inch))
        
        # 5. Insights Automáticos
        insights = [
            f"📊 Total de {metrics['total_membros']} membros cadastrados",
            f"✅ {metrics['taxa_ativos']:.1f}% dos membros estão ativos",
            f"📈 {metrics['novos_este_mes']} novos membros este mês",
        ]
        
        if metrics['crescimento'] > 0:
            insights.append(f"🚀 Crescimento de {metrics['crescimento']:.1f}% em novos membros")
        elif metrics['crescimento'] < 0:
            insights.append(f"⚠️ Redução de {abs(metrics['crescimento']):.1f}% em novos membros")
        
        story.extend(self.metrics.create_insights(insights))
        
        # 6. Nova página para lista detalhada
        story.append(PageBreak())
        story.append(Paragraph("📋 LISTA DETALHADA DE MEMBROS", self.styles['TituloPrincipal']))
        story.append(Spacer(1, 0.2*inch))
        
        # 7. Tabela de membros
        membros = Membro.objects.filter(is_active=True).order_by('nome')
        headers = ['Nome', 'Email', 'Status', 'Cargo', 'Idade']
        data = []
        
        for membro in membros:
            idade = ''
            if membro.data_nascimento:
                idade_calc = timezone.now().year - membro.data_nascimento.year
                idade = f"{idade_calc} anos"
            
            data.append([
                membro.nome,
                membro.email,
                membro.get_status_display(),
                membro.cargo.nome if membro.cargo else 'Sem cargo',
                idade
            ])
        
        story.extend(self.table.create_professional_table(
            headers, 
            data, 
            "Lista Completa de Membros"
        ))
        
        # 8. Construir PDF
        doc.build(story, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
        
        # Retornar PDF
        buffer.seek(0)
        return buffer.getvalue()
    
    def _add_footer(self, canvas, doc):
        """Adiciona rodapé às páginas"""
        canvas.saveState()
        
        # Obter número da página
        page_num = canvas.getPageNumber()
        
        # Desenhar rodapé
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(self.styles.colors['muted'])
        canvas.drawString(72, 50, f"Página {page_num} | Sistema Alfa+ v1.0.0 | {timezone.now().strftime('%d/%m/%Y %H:%M')}")
        
        canvas.restoreState()


class RelatorioFinanceiro(RelatorioBase):
    """Relatório Financeiro com design profissional"""
    
    def __init__(self, data_inicio=None, data_fim=None):
        super().__init__(data_inicio, data_fim)
        self.styles = PDFStyles()
        self.header = PDFHeader(self.styles)
        self.footer = PDFFooter(self.styles)
        self.charts = PDFCharts(self.styles)
        self.metrics = PDFMetrics(self.styles)
        self.table = PDFTable(self.styles)
        self.calculator = MetricsCalculator(data_inicio, data_fim)
    
    def get_estatisticas_financeiras(self):
        """Estatísticas financeiras usando o novo sistema"""
        return self.calculator.calculate_financial_metrics()
    
    def gerar_pdf(self):
        """Gera relatório PDF financeiro com design profissional"""
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Obter métricas
        metrics = self.get_estatisticas_financeiras()
        
        # Construir conteúdo do PDF
        story = []
        
        # 1. Cabeçalho
        titulo = "💰 RELATÓRIO FINANCEIRO"
        subtitulo = f"Período: {self.calculator.get_period_description()}"
        story.extend(self.header.create_header(titulo, subtitulo, timezone.now()))
        
        # 2. Resumo Executivo
        resumo_metrics = [
            {
                'label': 'Receitas',
                'value': self.calculator.format_currency(metrics['receitas']),
                'change': f"{metrics['crescimento_receitas']:+.1f}%" if metrics['crescimento_receitas'] != 0 else ''
            },
            {
                'label': 'Despesas',
                'value': self.calculator.format_currency(metrics['despesas']),
                'change': f"{metrics['crescimento_despesas']:+.1f}%" if metrics['crescimento_despesas'] != 0 else ''
            },
            {
                'label': 'Saldo',
                'value': self.calculator.format_currency(metrics['saldo']),
                'change': f"Margem: {metrics['margem_lucro']:.1f}%"
            }
        ]
        story.extend(self.metrics.create_metrics_summary(resumo_metrics))
        
        # 3. Gráfico de Receitas vs Despesas
        if metrics['receitas'] > 0 or metrics['despesas'] > 0:
            story.append(Paragraph("📊 RECEITAS VS DESPESAS", self.styles['CabecSecao']))
            chart_data = {
                'Receitas': metrics['receitas'],
                'Despesas': metrics['despesas']
            }
            chart = self.charts.create_bar_chart(
                chart_data,
                "Receitas vs Despesas",
                width=6*inch,
                height=3*inch
            )
            story.append(chart)
            story.append(Spacer(1, 0.2*inch))
        
        # 4. Top Categorias de Gastos
        if metrics['categorias_gastos']:
            story.append(Paragraph("💸 TOP CATEGORIAS DE GASTOS", self.styles['CabecSecao']))
            gastos_data = {}
            for item in metrics['categorias_gastos']:
                gastos_data[item['categoria']] = float(item['total'])
            
            chart = self.charts.create_pie_chart(
                gastos_data,
                "Categorias de Gastos",
                width=4*inch,
                height=3*inch
            )
            story.append(chart)
            story.append(Spacer(1, 0.2*inch))
        
        # 5. Insights Automáticos
        insights = [
            f"💰 Receitas: {self.calculator.format_currency(metrics['receitas'])}",
            f"💸 Despesas: {self.calculator.format_currency(metrics['despesas'])}",
            f"💚 Saldo: {self.calculator.format_currency(metrics['saldo'])}",
        ]
        
        if metrics['crescimento_receitas'] > 0:
            insights.append(f"📈 Receitas cresceram {metrics['crescimento_receitas']:.1f}%")
        elif metrics['crescimento_receitas'] < 0:
            insights.append(f"📉 Receitas diminuíram {abs(metrics['crescimento_receitas']):.1f}%")
        
        if metrics['margem_lucro'] > 30:
            insights.append(f"💚 Excelente margem de lucro: {metrics['margem_lucro']:.1f}%")
        elif metrics['margem_lucro'] < 10:
            insights.append(f"⚠️ Margem de lucro baixa: {metrics['margem_lucro']:.1f}%")
        
        story.extend(self.metrics.create_insights(insights))
        
        # 6. Nova página para lista detalhada
        story.append(PageBreak())
        story.append(Paragraph("📋 LISTA DETALHADA DE TRANSAÇÕES", self.styles['TituloPrincipal']))
        story.append(Spacer(1, 0.2*inch))
        
        # 7. Tabela de transações
        transacoes = Transacao.objects.filter(
            data__gte=self.data_inicio,
            data__lte=self.data_fim
        ).order_by('-data')
        
        headers = ['Data', 'Tipo', 'Categoria', 'Valor', 'Descrição']
        data = []
        
        for transacao in transacoes:
            tipo_icon = '📈' if transacao.tipo == 'entrada' else '📉'
            data.append([
                transacao.data.strftime('%d/%m/%Y'),
                f"{tipo_icon} {transacao.get_tipo_display()}",
                transacao.categoria,
                self.calculator.format_currency(float(transacao.valor)),
                transacao.descricao or '-'
            ])
        
        story.extend(self.table.create_professional_table(
            headers, 
            data, 
            "Transações do Período"
        ))
        
        # 8. Construir PDF
        doc.build(story, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
        
        # Retornar PDF
        buffer.seek(0)
        return buffer.getvalue()
    
    def _add_footer(self, canvas, doc):
        """Adiciona rodapé às páginas"""
        canvas.saveState()
        
        # Obter número da página
        page_num = canvas.getPageNumber()
        
        # Desenhar rodapé
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(self.styles.colors['muted'])
        canvas.drawString(72, 50, f"Página {page_num} | Sistema Alfa+ v1.0.0 | {timezone.now().strftime('%d/%m/%Y %H:%M')}")
        
        canvas.restoreState()


class RelatorioEventos(RelatorioBase):
    """Relatório de Eventos com design profissional"""
    
    def __init__(self, data_inicio=None, data_fim=None):
        super().__init__(data_inicio, data_fim)
        self.styles = PDFStyles()
        self.header = PDFHeader(self.styles)
        self.footer = PDFFooter(self.styles)
        self.charts = PDFCharts(self.styles)
        self.metrics = PDFMetrics(self.styles)
        self.table = PDFTable(self.styles)
        self.calculator = MetricsCalculator(data_inicio, data_fim)
    
    def get_estatisticas_eventos(self):
        """Estatísticas de eventos usando o novo sistema"""
        return self.calculator.calculate_event_metrics()
    
    def gerar_pdf(self):
        """Gera relatório PDF de eventos com design profissional"""
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Obter métricas
        metrics = self.get_estatisticas_eventos()
        
        # Construir conteúdo do PDF
        story = []
        
        # 1. Cabeçalho
        titulo = "📅 RELATÓRIO DE EVENTOS"
        subtitulo = f"Período: {self.calculator.get_period_description()}"
        story.extend(self.header.create_header(titulo, subtitulo, timezone.now()))
        
        # 2. Resumo Executivo
        resumo_metrics = [
            {
                'label': 'Total de Eventos',
                'value': str(metrics['total_eventos']),
                'change': ''
            },
            {
                'label': 'Eventos Realizados',
                'value': str(metrics['eventos_realizados']),
                'change': ''
            },
            {
                'label': 'Eventos Agendados',
                'value': str(metrics['eventos_agendados']),
                'change': ''
            },
            {
                'label': 'Participação Média',
                'value': f"{metrics['participacao_media']:.1f} pessoas",
                'change': ''
            }
        ]
        story.extend(self.metrics.create_metrics_summary(resumo_metrics))
        
        # 3. Gráfico de Status dos Eventos
        if metrics['total_eventos'] > 0:
            story.append(Paragraph("📊 STATUS DOS EVENTOS", self.styles['CabecSecao']))
            status_data = {
                'Realizados': metrics['eventos_realizados'],
                'Agendados': metrics['eventos_agendados']
            }
            chart = self.charts.create_pie_chart(
                status_data,
                "Status dos Eventos",
                width=4*inch,
                height=3*inch
            )
            story.append(chart)
            story.append(Spacer(1, 0.2*inch))
        
        # 4. Gráfico de Eventos por Mês
        if metrics['eventos_por_mes'] and any(metrics['eventos_por_mes'].values()):
            story.append(Paragraph("📈 EVENTOS POR MÊS", self.styles['CabecSecao']))
            chart = self.charts.create_bar_chart(
                metrics['eventos_por_mes'],
                "Eventos por Mês",
                width=6*inch,
                height=3*inch
            )
            story.append(chart)
            story.append(Spacer(1, 0.2*inch))
        
        # 5. Insights Automáticos
        insights = [
            f"📅 Total de {metrics['total_eventos']} eventos no período",
            f"✅ {metrics['eventos_realizados']} eventos já realizados",
            f"📋 {metrics['eventos_agendados']} eventos agendados",
        ]
        
        if metrics['participacao_media'] > 20:
            insights.append(f"🎉 Alta participação média: {metrics['participacao_media']:.1f} pessoas por evento")
        elif metrics['participacao_media'] < 10:
            insights.append(f"📢 Baixa participação: {metrics['participacao_media']:.1f} pessoas por evento")
        
        if metrics['eventos_agendados'] > 0:
            insights.append(f"📅 {metrics['eventos_agendados']} eventos agendados para o futuro")
        
        story.extend(self.metrics.create_insights(insights))
        
        # 6. Nova página para lista detalhada
        story.append(PageBreak())
        story.append(Paragraph("📋 LISTA DETALHADA DE EVENTOS", self.styles['TituloPrincipal']))
        story.append(Spacer(1, 0.2*inch))
        
        # 7. Tabela de eventos
        eventos = Evento.objects.filter(
            data__gte=self.data_inicio,
            data__lte=self.data_fim
        ).order_by('-data')
        
        headers = ['Título', 'Data', 'Status', 'Participantes', 'Local']
        data = []
        
        for evento in eventos:
            # Determinar status
            agora = timezone.now()
            status = '✅ Realizado' if evento.data < agora else '📅 Agendado'
            
            # Contar participantes
            participantes = EventoPresenca.objects.filter(
                evento=evento,
                confirmado=True
            ).count()
            
            data.append([
                evento.titulo,
                evento.data.strftime('%d/%m/%Y %H:%M'),
                status,
                str(participantes),
                evento.local or '-'
            ])
        
        story.extend(self.table.create_professional_table(
            headers, 
            data, 
            "Eventos do Período"
        ))
        
        # 8. Construir PDF
        doc.build(story, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
        
        # Retornar PDF
        buffer.seek(0)
        return buffer.getvalue()
    
    def _add_footer(self, canvas, doc):
        """Adiciona rodapé às páginas"""
        canvas.saveState()
        
        # Obter número da página
        page_num = canvas.getPageNumber()
        
        # Desenhar rodapé
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(self.styles.colors['muted'])
        canvas.drawString(72, 50, f"Página {page_num} | Sistema Alfa+ v1.0.0 | {timezone.now().strftime('%d/%m/%Y %H:%M')}")
        
        canvas.restoreState()


# Classes auxiliares para compatibilidade
class RelatorioGeral(RelatorioBase):
    """Relatório geral do sistema"""
    pass

class ExportadorDados(RelatorioBase):
    """Exportador de dados"""
    pass
