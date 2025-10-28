"""
Sistema de Templates e Estilos para PDFs - Alfa+
Templates profissionais e reutilizáveis para geração de relatórios
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader
from datetime import datetime
import io
import os
from django.conf import settings

class PDFStyles:
    """Classe com estilos padronizados para PDFs"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def __getitem__(self, key):
        """Permite acesso aos estilos usando PDFStyles['NomeEstilo']"""
        return self.styles[key]
    
    def _create_custom_styles(self):
        """Cria estilos customizados para o sistema Alfa+"""
        
        # Cores da igreja
        self.colors = {
            'primary': colors.HexColor('#dc2626'),      # Vermelho principal
            'secondary': colors.HexColor('#ef4444'),    # Vermelho claro
            'accent': colors.HexColor('#f59e0b'),       # Dourado
            'success': colors.HexColor('#10b981'),      # Verde
            'warning': colors.HexColor('#f59e0b'),      # Amarelo
            'danger': colors.HexColor('#dc2626'),       # Vermelho
            'light': colors.HexColor('#fef2f2'),        # Vermelho muito claro
            'dark': colors.HexColor('#1f2937'),         # Cinza escuro
            'text': colors.HexColor('#374151'),         # Texto
            'muted': colors.HexColor('#6b7280'),        # Texto secundário
        }
        
        # Estilo do título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.colors['primary'],
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo do subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.colors['secondary'],
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Estilo do cabeçalho de seção
        self.styles.add(ParagraphStyle(
            name='CabecSecao',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=self.colors['primary'],
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=self.colors['primary'],
            borderPadding=5,
            backColor=self.colors['light']
        ))
        
        # Estilo do texto normal
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.colors['text'],
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Estilo do texto pequeno
        self.styles.add(ParagraphStyle(
            name='TextoPequeno',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.colors['muted'],
            spaceAfter=4,
            fontName='Helvetica'
        ))
        
        # Estilo do texto destacado
        self.styles.add(ParagraphStyle(
            name='TextoDestaque',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=self.colors['primary'],
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo do rodapé
        self.styles.add(ParagraphStyle(
            name='Rodape',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.colors['muted'],
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

class PDFHeader:
    """Classe para gerar cabeçalhos profissionais"""
    
    def __init__(self, styles):
        self.styles = styles
    
    def create_header(self, titulo, subtitulo=None, data_geracao=None):
        """Cria cabeçalho profissional para o PDF"""
        elements = []
        
        # Logo da igreja (se existir)
        logo_path = os.path.join(settings.MEDIA_ROOT, 'logo_igreja.png')
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2*inch, height=1*inch)
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Título principal
        elements.append(Paragraph(titulo, self.styles['TituloPrincipal']))
        
        # Subtítulo (se fornecido)
        if subtitulo:
            elements.append(Paragraph(subtitulo, self.styles['Subtitulo']))
        
        # Data de geração
        if data_geracao:
            data_str = data_geracao.strftime("%d/%m/%Y às %H:%M")
            elements.append(Paragraph(f"Gerado em: {data_str}", self.styles['TextoPequeno']))
        
        # Linha divisória
        elements.append(Spacer(1, 0.1*inch))
        elements.append(self._create_divider())
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_divider(self):
        """Cria linha divisória elegante"""
        return Table(
            [['']],
            colWidths=[7*inch],
            rowHeights=[0.01*inch],
            style=TableStyle([
                ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#1e40af')),
            ])
        )

class PDFFooter:
    """Classe para gerar rodapés informativos"""
    
    def __init__(self, styles):
        self.styles = styles
    
    def create_footer(self, pagina_atual, total_paginas, sistema="Sistema Alfa+", versao="1.0.0"):
        """Cria rodapé informativo para o PDF"""
        elements = []
        
        # Linha divisória superior
        elements.append(Spacer(1, 0.1*inch))
        elements.append(self._create_divider())
        elements.append(Spacer(1, 0.1*inch))
        
        # Informações do rodapé
        footer_text = f"Página {pagina_atual} de {total_paginas} | {sistema} v{versao} | {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        elements.append(Paragraph(footer_text, self.styles['Rodape']))
        
        return elements
    
    def _create_divider(self):
        """Cria linha divisória elegante"""
        return Table(
            [['']],
            colWidths=[7*inch],
            rowHeights=[0.01*inch],
            style=TableStyle([
                ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#1e40af')),
            ])
        )

class PDFCharts:
    """Classe para gerar gráficos nos PDFs"""
    
    def __init__(self, styles):
        self.styles = styles
        self.colors = styles.colors
    
    def create_pie_chart(self, data, title, width=4*inch, height=3*inch):
        """Cria gráfico de pizza"""
        drawing = Drawing(width, height)
        
        # Cores para o gráfico
        chart_colors = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['accent'],
            self.colors['success'],
            self.colors['warning'],
            self.colors['danger']
        ]
        
        pie = Pie()
        pie.x = 0.5*inch
        pie.y = 0.5*inch
        pie.width = width - 1*inch
        pie.height = height - 1*inch
        
        # Dados do gráfico
        labels = list(data.keys())
        values = list(data.values())
        
        pie.data = values
        pie.labels = labels
        pie.slices.strokeWidth = 0.5
        pie.slices.strokeColor = colors.white
        
        # Aplicar cores
        for i, color in enumerate(chart_colors[:len(labels)]):
            pie.slices[i].fillColor = color
        
        drawing.add(pie)
        return drawing
    
    def create_bar_chart(self, data, title, width=6*inch, height=3*inch):
        """Cria gráfico de barras"""
        drawing = Drawing(width, height)
        
        chart = VerticalBarChart()
        chart.x = 0.5*inch
        chart.y = 0.5*inch
        chart.width = width - 1*inch
        chart.height = height - 1*inch
        
        # Dados do gráfico
        labels = list(data.keys())
        values = list(data.values())
        
        chart.data = [values]
        chart.categoryAxis.categoryNames = labels
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(values) * 1.1
        
        # Estilo do gráfico
        chart.bars[0].fillColor = self.colors['primary']
        chart.bars[0].strokeColor = colors.white
        chart.bars[0].strokeWidth = 1
        
        drawing.add(chart)
        return drawing

class PDFMetrics:
    """Classe para gerar métricas e insights"""
    
    def __init__(self, styles):
        self.styles = styles
    
    def create_metrics_summary(self, metrics):
        """Cria resumo de métricas destacadas"""
        elements = []
        
        # Título da seção
        elements.append(Paragraph("📊 RESUMO EXECUTIVO", self.styles['CabecSecao']))
        
        # Criar tabela de métricas
        data = []
        for metric in metrics:
            data.append([
                Paragraph(metric['label'], self.styles['TextoDestaque']),
                Paragraph(metric['value'], self.styles['TextoDestaque']),
                Paragraph(metric.get('change', ''), self.styles['TextoPequeno'])
            ])
        
        table = Table(data, colWidths=[3*inch, 2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_insights(self, insights):
        """Cria seção de insights automáticos"""
        elements = []
        
        # Título da seção
        elements.append(Paragraph("💡 INSIGHTS AUTOMÁTICOS", self.styles['CabecSecao']))
        
        # Lista de insights
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", self.styles['TextoNormal']))
        
        elements.append(Spacer(1, 0.2*inch))
        return elements

class PDFTable:
    """Classe para criar tabelas profissionais"""
    
    def __init__(self, styles):
        self.styles = styles
    
    def create_professional_table(self, headers, data, title=None):
        """Cria tabela profissional com estilo"""
        elements = []
        
        if title:
            elements.append(Paragraph(title, self.styles['CabecSecao']))
        
        # Preparar dados da tabela
        table_data = [headers] + data
        
        # Criar tabela
        table = Table(table_data, repeatRows=1)
        
        # Aplicar estilo
        table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Dados
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            
            # Alternância de cores nas linhas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
