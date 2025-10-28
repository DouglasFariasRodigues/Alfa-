"""
Utilitários para Cálculos de Métricas e Insights - Alfa+
Funções auxiliares para geração de relatórios inteligentes
"""

from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Membro, Evento, Transacao, EventoPresenca

class MetricsCalculator:
    """Classe para calcular métricas e insights dos dados"""
    
    def __init__(self, data_inicio=None, data_fim=None):
        self.data_inicio = data_inicio or (timezone.now() - timedelta(days=30))
        self.data_fim = data_fim or timezone.now()
        self.agora = timezone.now()
    
    def calculate_member_metrics(self):
        """Calcula métricas de membros"""
        # Dados básicos
        total_membros = Membro.objects.filter(is_active=True).count()
        membros_ativos = Membro.objects.filter(is_active=True, status='ativo').count()
        membros_inativos = Membro.objects.filter(is_active=True, status='inativo').count()
        
        # Membros por status
        status_distribution = {}
        for status, _ in Membro.STATUS_CHOICES:
            count = Membro.objects.filter(is_active=True, status=status).count()
            if count > 0:
                status_distribution[status.title()] = count
        
        # Novos membros este mês
        inicio_mes = self.agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        novos_este_mes = Membro.objects.filter(
            is_active=True,
            created_at__gte=inicio_mes
        ).count()
        
        # Novos membros mês anterior
        mes_anterior_inicio = (inicio_mes - timedelta(days=1)).replace(day=1)
        mes_anterior_fim = inicio_mes - timedelta(days=1)
        novos_mes_anterior = Membro.objects.filter(
            is_active=True,
            created_at__gte=mes_anterior_inicio,
            created_at__lte=mes_anterior_fim
        ).count()
        
        # Calcular crescimento
        crescimento = 0
        if novos_mes_anterior > 0:
            crescimento = ((novos_este_mes - novos_mes_anterior) / novos_mes_anterior) * 100
        
        # Faixa etária (simulação - seria melhor com campo idade)
        membros_com_data_nasc = Membro.objects.filter(
            is_active=True,
            data_nascimento__isnull=False
        )
        
        faixas_etarias = {
            '18-25': 0,
            '26-35': 0,
            '36-50': 0,
            '51-65': 0,
            '65+': 0
        }
        
        for membro in membros_com_data_nasc:
            if membro.data_nascimento:
                idade = self.agora.year - membro.data_nascimento.year
                if 18 <= idade <= 25:
                    faixas_etarias['18-25'] += 1
                elif 26 <= idade <= 35:
                    faixas_etarias['26-35'] += 1
                elif 36 <= idade <= 50:
                    faixas_etarias['36-50'] += 1
                elif 51 <= idade <= 65:
                    faixas_etarias['51-65'] += 1
                else:
                    faixas_etarias['65+'] += 1
        
        return {
            'total_membros': total_membros,
            'membros_ativos': membros_ativos,
            'membros_inativos': membros_inativos,
            'status_distribution': status_distribution,
            'novos_este_mes': novos_este_mes,
            'crescimento': crescimento,
            'faixas_etarias': faixas_etarias,
            'taxa_ativos': (membros_ativos / total_membros * 100) if total_membros > 0 else 0
        }
    
    def calculate_financial_metrics(self):
        """Calcula métricas financeiras"""
        # Período atual
        transacoes_periodo = Transacao.objects.filter(
            data__gte=self.data_inicio,
            data__lte=self.data_fim
        )
        
        # Receitas e despesas
        receitas = transacoes_periodo.filter(tipo='entrada').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0')
        
        despesas = transacoes_periodo.filter(tipo='saida').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0')
        
        saldo = receitas - despesas
        
        # Comparação com período anterior
        periodo_anterior_inicio = self.data_inicio - (self.data_fim - self.data_inicio)
        periodo_anterior_fim = self.data_inicio
        
        transacoes_anterior = Transacao.objects.filter(
            data__gte=periodo_anterior_inicio,
            data__lte=periodo_anterior_fim
        )
        
        receitas_anterior = transacoes_anterior.filter(tipo='entrada').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0')
        
        despesas_anterior = transacoes_anterior.filter(tipo='saida').aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0')
        
        # Calcular crescimento
        crescimento_receitas = 0
        if receitas_anterior > 0:
            crescimento_receitas = ((receitas - receitas_anterior) / receitas_anterior) * 100
        
        crescimento_despesas = 0
        if despesas_anterior > 0:
            crescimento_despesas = ((despesas - despesas_anterior) / despesas_anterior) * 100
        
        # Categorias mais gastas
        categorias_gastos = transacoes_periodo.filter(tipo='saida').values('categoria').annotate(
            total=Sum('valor')
        ).order_by('-total')[:5]
        
        # Categorias mais recebidas
        categorias_receitas = transacoes_periodo.filter(tipo='entrada').values('categoria').annotate(
            total=Sum('valor')
        ).order_by('-total')[:5]
        
        return {
            'receitas': float(receitas),
            'despesas': float(despesas),
            'saldo': float(saldo),
            'crescimento_receitas': crescimento_receitas,
            'crescimento_despesas': crescimento_despesas,
            'categorias_gastos': list(categorias_gastos),
            'categorias_receitas': list(categorias_receitas),
            'margem_lucro': (float(saldo) / float(receitas) * 100) if receitas > 0 else 0
        }
    
    def calculate_event_metrics(self):
        """Calcula métricas de eventos"""
        # Eventos do período
        eventos_periodo = Evento.objects.filter(
            data__gte=self.data_inicio,
            data__lte=self.data_fim
        )
        
        total_eventos = eventos_periodo.count()
        eventos_realizados = eventos_periodo.filter(data__lt=self.agora).count()
        eventos_agendados = eventos_periodo.filter(data__gte=self.agora).count()
        
        # Participação média
        presencas_periodo = EventoPresenca.objects.filter(
            evento__in=eventos_periodo,
            confirmado=True
        )
        
        participacao_media = 0
        if total_eventos > 0:
            participacao_media = presencas_periodo.count() / total_eventos
        
        # Eventos mais populares
        eventos_populares = eventos_periodo.annotate(
            total_presencas=Count('presencas', filter=Q(presencas__confirmado=True))
        ).order_by('-total_presencas')[:5]
        
        # Eventos por mês (últimos 6 meses)
        eventos_por_mes = {}
        for i in range(6):
            mes = self.agora - timedelta(days=30*i)
            inicio_mes = mes.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            count = Evento.objects.filter(
                data__gte=inicio_mes,
                data__lte=fim_mes
            ).count()
            
            eventos_por_mes[inicio_mes.strftime('%m/%Y')] = count
        
        return {
            'total_eventos': total_eventos,
            'eventos_realizados': eventos_realizados,
            'eventos_agendados': eventos_agendados,
            'participacao_media': participacao_media,
            'eventos_populares': list(eventos_populares),
            'eventos_por_mes': eventos_por_mes
        }
    
    def generate_insights(self, member_metrics, financial_metrics, event_metrics):
        """Gera insights automáticos baseados nas métricas"""
        insights = []
        
        # Insights de membros
        if member_metrics['crescimento'] > 0:
            insights.append(f"📈 Crescimento positivo de {member_metrics['crescimento']:.1f}% em novos membros este mês")
        elif member_metrics['crescimento'] < 0:
            insights.append(f"📉 Redução de {abs(member_metrics['crescimento']):.1f}% em novos membros este mês")
        
        if member_metrics['taxa_ativos'] > 80:
            insights.append(f"✅ Excelente engajamento: {member_metrics['taxa_ativos']:.1f}% dos membros estão ativos")
        elif member_metrics['taxa_ativos'] < 60:
            insights.append(f"⚠️ Atenção: Apenas {member_metrics['taxa_ativos']:.1f}% dos membros estão ativos")
        
        # Insights financeiros
        if financial_metrics['crescimento_receitas'] > 0:
            insights.append(f"💰 Receitas cresceram {financial_metrics['crescimento_receitas']:.1f}% em relação ao período anterior")
        elif financial_metrics['crescimento_receitas'] < 0:
            insights.append(f"📉 Receitas diminuíram {abs(financial_metrics['crescimento_receitas']):.1f}% em relação ao período anterior")
        
        if financial_metrics['margem_lucro'] > 30:
            insights.append(f"💚 Excelente margem de lucro: {financial_metrics['margem_lucro']:.1f}%")
        elif financial_metrics['margem_lucro'] < 10:
            insights.append(f"⚠️ Margem de lucro baixa: {financial_metrics['margem_lucro']:.1f}%")
        
        # Insights de eventos
        if event_metrics['participacao_media'] > 20:
            insights.append(f"🎉 Alta participação média em eventos: {event_metrics['participacao_media']:.1f} pessoas por evento")
        elif event_metrics['participacao_media'] < 10:
            insights.append(f"📢 Baixa participação em eventos: {event_metrics['participacao_media']:.1f} pessoas por evento")
        
        if event_metrics['eventos_agendados'] > 0:
            insights.append(f"📅 {event_metrics['eventos_agendados']} eventos agendados para o futuro")
        
        return insights
    
    def format_currency(self, value):
        """Formata valor monetário"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def format_percentage(self, value):
        """Formata porcentagem"""
        return f"{value:.1f}%"
    
    def get_period_description(self):
        """Retorna descrição do período"""
        if self.data_inicio == self.data_fim:
            return f"em {self.data_inicio.strftime('%d/%m/%Y')}"
        else:
            return f"de {self.data_inicio.strftime('%d/%m/%Y')} a {self.data_fim.strftime('%d/%m/%Y')}"
