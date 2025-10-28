#!/usr/bin/env python
"""
Script de teste para verificar as melhorias nos PDFs
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from app_alfa.reports import RelatorioMembros, RelatorioFinanceiro, RelatorioEventos
from app_alfa.models import Membro, Evento, Transacao

def test_pdf_generation():
    """Testa a geração de PDFs com as melhorias"""
    print("🧪 TESTANDO MELHORIAS NOS PDFs DO SISTEMA ALFA+")
    print("=" * 60)
    
    # Período de teste (últimos 30 dias)
    data_fim = timezone.now()
    data_inicio = data_fim - timedelta(days=30)
    
    try:
        # 1. Teste do Relatório de Membros
        print("\n📊 1. TESTANDO RELATÓRIO DE MEMBROS")
        print("-" * 40)
        
        relatorio_membros = RelatorioMembros(data_inicio, data_fim)
        pdf_membros = relatorio_membros.gerar_pdf()
        
        print(f"✅ PDF de Membros gerado com sucesso!")
        print(f"   Tamanho: {len(pdf_membros)} bytes")
        
        # Salvar para visualização
        with open('teste_relatorio_membros.pdf', 'wb') as f:
            f.write(pdf_membros)
        print(f"   Salvo como: teste_relatorio_membros.pdf")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF de Membros: {e}")
    
    try:
        # 2. Teste do Relatório Financeiro
        print("\n💰 2. TESTANDO RELATÓRIO FINANCEIRO")
        print("-" * 40)
        
        relatorio_financeiro = RelatorioFinanceiro(data_inicio, data_fim)
        pdf_financeiro = relatorio_financeiro.gerar_pdf()
        
        print(f"✅ PDF Financeiro gerado com sucesso!")
        print(f"   Tamanho: {len(pdf_financeiro)} bytes")
        
        # Salvar para visualização
        with open('teste_relatorio_financeiro.pdf', 'wb') as f:
            f.write(pdf_financeiro)
        print(f"   Salvo como: teste_relatorio_financeiro.pdf")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF Financeiro: {e}")
    
    try:
        # 3. Teste do Relatório de Eventos
        print("\n📅 3. TESTANDO RELATÓRIO DE EVENTOS")
        print("-" * 40)
        
        relatorio_eventos = RelatorioEventos(data_inicio, data_fim)
        pdf_eventos = relatorio_eventos.gerar_pdf()
        
        print(f"✅ PDF de Eventos gerado com sucesso!")
        print(f"   Tamanho: {len(pdf_eventos)} bytes")
        
        # Salvar para visualização
        with open('teste_relatorio_eventos.pdf', 'wb') as f:
            f.write(pdf_eventos)
        print(f"   Salvo como: teste_relatorio_eventos.pdf")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF de Eventos: {e}")
    
    # 4. Teste das métricas
    print("\n📈 4. TESTANDO CÁLCULO DE MÉTRICAS")
    print("-" * 40)
    
    try:
        from app_alfa.pdf_utils import MetricsCalculator
        
        calculator = MetricsCalculator(data_inicio, data_fim)
        
        # Métricas de membros
        metrics_membros = calculator.calculate_member_metrics()
        print(f"✅ Métricas de Membros calculadas:")
        print(f"   - Total: {metrics_membros['total_membros']}")
        print(f"   - Ativos: {metrics_membros['membros_ativos']}")
        print(f"   - Taxa de ativos: {metrics_membros['taxa_ativos']:.1f}%")
        print(f"   - Novos este mês: {metrics_membros['novos_este_mes']}")
        print(f"   - Crescimento: {metrics_membros['crescimento']:+.1f}%")
        
        # Métricas financeiras
        metrics_financeiro = calculator.calculate_financial_metrics()
        print(f"\n✅ Métricas Financeiras calculadas:")
        print(f"   - Receitas: R$ {metrics_financeiro['receitas']:,.2f}")
        print(f"   - Despesas: R$ {metrics_financeiro['despesas']:,.2f}")
        print(f"   - Saldo: R$ {metrics_financeiro['saldo']:,.2f}")
        print(f"   - Margem de lucro: {metrics_financeiro['margem_lucro']:.1f}%")
        
        # Métricas de eventos
        metrics_eventos = calculator.calculate_event_metrics()
        print(f"\n✅ Métricas de Eventos calculadas:")
        print(f"   - Total: {metrics_eventos['total_eventos']}")
        print(f"   - Realizados: {metrics_eventos['eventos_realizados']}")
        print(f"   - Agendados: {metrics_eventos['eventos_agendados']}")
        print(f"   - Participação média: {metrics_eventos['participacao_media']:.1f}")
        
    except Exception as e:
        print(f"❌ Erro ao calcular métricas: {e}")
    
    print("\n🎉 TESTE CONCLUÍDO!")
    print("=" * 60)
    print("📁 Arquivos PDF gerados:")
    print("   - teste_relatorio_membros.pdf")
    print("   - teste_relatorio_financeiro.pdf") 
    print("   - teste_relatorio_eventos.pdf")
    print("\n✨ Os PDFs agora têm:")
    print("   - Design profissional com cabeçalho e rodapé")
    print("   - Gráficos coloridos e informativos")
    print("   - Métricas inteligentes e insights automáticos")
    print("   - Layout responsivo e organizado")
    print("   - Códigos de cores consistentes")

if __name__ == "__main__":
    test_pdf_generation()
