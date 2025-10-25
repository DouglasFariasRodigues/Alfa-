"""
Views para Relatórios e Analytics - Alfa+
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .reports import (
    RelatorioMembros, 
    RelatorioFinanceiro, 
    RelatorioEventos, 
    RelatorioGeral,
    ExportadorDados
)


class RelatorioMembrosView(View):
    """View para relatórios de membros"""
    
    def get(self, request):
        """Gera relatório PDF de membros"""
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Converter strings para datetime se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        relatorio = RelatorioMembros(data_inicio, data_fim)
        return relatorio.gerar_pdf()


class RelatorioFinanceiroView(View):
    """View para relatórios financeiros"""
    
    def get(self, request):
        """Gera relatório PDF financeiro"""
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Converter strings para datetime se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        relatorio = RelatorioFinanceiro(data_inicio, data_fim)
        return relatorio.gerar_pdf()


class RelatorioEventosView(View):
    """View para relatórios de eventos"""
    
    def get(self, request):
        """Gera relatório PDF de eventos"""
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Converter strings para datetime se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        relatorio = RelatorioEventos(data_inicio, data_fim)
        return relatorio.gerar_pdf()


class DashboardView(View):
    """View para dashboard com dados gerais"""
    
    def get(self, request):
        """Retorna dados para o dashboard"""
        relatorio = RelatorioGeral()
        dados = relatorio.get_dashboard_data()
        return JsonResponse(dados)


class EstatisticasMembrosView(View):
    """View para estatísticas de membros (API)"""
    
    def get(self, request):
        """Retorna estatísticas de membros em JSON"""
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Converter strings para datetime se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        relatorio = RelatorioMembros(data_inicio, data_fim)
        dados = relatorio.get_estatisticas_membros()
        return JsonResponse(dados)


class EstatisticasFinanceirasView(View):
    """View para estatísticas financeiras (API)"""
    
    def get(self, request):
        """Retorna estatísticas financeiras em JSON"""
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Converter strings para datetime se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        relatorio = RelatorioFinanceiro(data_inicio, data_fim)
        dados = relatorio.get_estatisticas_financeiras()
        return JsonResponse(dados)


class EstatisticasEventosView(View):
    """View para estatísticas de eventos (API)"""
    
    def get(self, request):
        """Retorna estatísticas de eventos em JSON"""
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Converter strings para datetime se fornecidas
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        relatorio = RelatorioEventos(data_inicio, data_fim)
        dados = relatorio.get_estatisticas_eventos()
        return JsonResponse(dados)


class ExportarMembrosView(View):
    """View para exportar membros em CSV"""
    
    def get(self, request):
        """Exporta membros para CSV"""
        return ExportadorDados.exportar_membros_csv()


class ExportarTransacoesView(View):
    """View para exportar transações em CSV"""
    
    def get(self, request):
        """Exporta transações para CSV"""
        return ExportadorDados.exportar_transacoes_csv()
