"""
Testes de integração para ofertas e transações financeiras.
Valida fluxos completos de entrada/saída de dinheiro.
"""
import pytest
from django.test import TestCase, TransactionTestCase
from decimal import Decimal
from django.utils import timezone

from app_alfa.models import (
    Admin, Oferta, Transacao, ONG, DistribuicaoOferta, Membro
)


@pytest.mark.integration
@pytest.mark.finance
class TestOfertasIntegration(TransactionTestCase):
    """Testes de integração para fluxo de ofertas"""
    
    reset_sequences = True
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.ong = ONG.objects.create(
            nome="ONG Assistência",
            cnpj="12.345.678/0001-90"
        )
    
    def test_oferta_creation_flow(self):
        """Testa fluxo completo de criação de oferta"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta para caridade",
            registrado_por=self.admin,
            is_publico=True
        )
        
        assert oferta.valor == Decimal("1000.00")
        assert oferta.registrado_por == self.admin
        assert oferta.is_publico is True
    
    def test_oferta_distribution_flow(self):
        """Testa fluxo de distribuição de oferta para ONG"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta para distribuir",
            registrado_por=self.admin
        )
        
        distribuicao = DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=self.ong,
            valor=Decimal("1000.00"),
            destino=self.ong.nome
        )
        
        assert distribuicao.oferta == oferta
        assert distribuicao.valor == Decimal("1000.00")
        assert distribuicao.ong == self.ong
    
    def test_multiple_distributions_single_oferta(self):
        """Testa distribuição de uma oferta para múltiplas ONGs"""
        ong2 = ONG.objects.create(
            nome="ONG Educação",
            cnpj="98.765.432/0001-11"
        )
        
        oferta = Oferta.objects.create(
            valor=Decimal("3000.00"),
            descricao="Oferta para múltiplas ONGs",
            registrado_por=self.admin
        )
        
        dist1 = DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=self.ong,
            valor=Decimal("1500.00"),
            destino=self.ong.nome
        )
        
        dist2 = DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong2,
            valor=Decimal("1500.00"),
            destino=ong2.nome
        )
        
        total_distribuido = (
            DistribuicaoOferta.objects.filter(oferta=oferta)
            .values_list('valor', flat=True)
        )
        
        assert len(list(total_distribuido)) == 2
        assert sum(total_distribuido) == Decimal("3000.00")
    
    def test_private_oferta_not_visible(self):
        """Testa que ofertas privadas não aparecem em listagens públicas"""
        oferta_publica = Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta pública",
            registrado_por=self.admin,
            is_publico=True
        )
        
        oferta_privada = Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta privada",
            registrado_por=self.admin,
            is_publico=False
        )
        
        ofertas_publicas = Oferta.objects.filter(is_publico=True)
        
        assert oferta_publica in ofertas_publicas
        assert oferta_privada not in ofertas_publicas


@pytest.mark.integration
@pytest.mark.finance
@pytest.mark.django_db
class TestTransacoesIntegration(TransactionTestCase):
    """Testes de integração para transações financeiras"""
    
    reset_sequences = True
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_transacao_entrada_creation(self):
        """Testa criação de transação de entrada"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Doação",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            descricao="Doação recebida",
            registrado_por=self.admin
        )
        
        assert transacao.tipo == Transacao.ENTRADA
        assert transacao.valor == Decimal("500.00")
    
    def test_transacao_saida_creation(self):
        """Testa criação de transação de saída"""
        transacao = Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa Operacional",
            valor=Decimal("100.00"),
            data=timezone.now().date(),
            descricao="Despesa operacional",
            registrado_por=self.admin
        )
        
        assert transacao.tipo == Transacao.SAIDA
        assert transacao.valor == Decimal("100.00")
    
    def test_multiple_transacoes_flow(self):
        """Testa fluxo com múltiplas transações"""
        # Entradas
        entrada1 = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Doação",
            valor=Decimal("1000.00"),
            data=timezone.now().date(),
            descricao="Doação 1",
            registrado_por=self.admin
        )
        
        entrada2 = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            descricao="Doação 2",
            registrado_por=self.admin
        )
        
        # Saídas
        saida1 = Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa Operacional",
            valor=Decimal("200.00"),
            data=timezone.now().date(),
            descricao="Despesa 1",
            registrado_por=self.admin
        )
        
        entradas = Transacao.objects.filter(tipo=Transacao.ENTRADA)
        saidas = Transacao.objects.filter(tipo=Transacao.SAIDA)
        
        assert entradas.count() == 2
        assert saidas.count() == 1
        
        total_entrada = sum(t.valor for t in entradas)
        total_saida = sum(t.valor for t in saidas)
        
        assert total_entrada == Decimal("1500.00")
        assert total_saida == Decimal("200.00")
        assert total_entrada > total_saida

