"""
Testes para transações e análise financeira.
Testes de modelos de Oferta, Doação e Transacao.
"""
import pytest
from django.test import TestCase
from decimal import Decimal
from django.utils import timezone

from app_alfa.models import (
    Admin, Oferta, DistribuicaoOferta, ONG, Membro, 
    Doacao, Transacao
)


@pytest.mark.unit
@pytest.mark.finance
class TestOfertaAdvanced(TestCase):
    """Testes avançados para Oferta"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_oferta_total_value(self):
        """Testa valor total de ofertas"""
        Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta 1",
            registrado_por=self.admin
        )
        Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta 2",
            registrado_por=self.admin
        )
        
        total = sum(o.valor for o in Oferta.objects.all())
        assert total == Decimal("1500.00")
    
    def test_oferta_distribuicao_tracking(self):
        """Testa rastreamento de distribuição de ofertas"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta",
            registrado_por=self.admin
        )
        
        ong1 = ONG.objects.create(nome="ONG 1", cnpj="11.111.111/0001-11")
        ong2 = ONG.objects.create(nome="ONG 2", cnpj="22.222.222/0001-22")
        
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong1,
            valor=Decimal("600.00"),
            destino="ONG 1"
        )
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong2,
            valor=Decimal("400.00"),
            destino="ONG 2"
        )
        
        total_distribuido = sum(d.valor for d in oferta.distribuicoes.all())
        assert total_distribuido == Decimal("1000.00")
    
    def test_oferta_public_private(self):
        """Testa visibilidade de ofertas (pública/privada)"""
        oferta_publica = Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta Pública",
            registrado_por=self.admin,
            is_publico=True
        )
        
        oferta_privada = Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta Privada",
            registrado_por=self.admin,
            is_publico=False
        )
        
        assert oferta_publica.is_publico is True
        assert oferta_privada.is_publico is False
    
    def test_oferta_filter_by_visibility(self):
        """Testa filtro de ofertas por visibilidade"""
        Oferta.objects.create(
            valor=Decimal("100.00"),
            descricao="Oferta 1",
            registrado_por=self.admin,
            is_publico=True
        )
        Oferta.objects.create(
            valor=Decimal("100.00"),
            descricao="Oferta 2",
            registrado_por=self.admin,
            is_publico=False
        )
        
        publicas = Oferta.objects.filter(is_publico=True).count()
        privadas = Oferta.objects.filter(is_publico=False).count()
        
        assert publicas == 1
        assert privadas == 1
    
    def test_oferta_admin_tracking(self):
        """Testa rastreamento do admin que registrou"""
        admin2 = Admin.objects.create(
            nome="Admin 2",
            email="admin2@test.com",
            senha="456"
        )
        
        oferta1 = Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta",
            registrado_por=self.admin
        )
        
        oferta2 = Oferta.objects.create(
            valor=Decimal("500.00"),
            descricao="Oferta",
            registrado_por=admin2
        )
        
        assert oferta1.registrado_por == self.admin
        assert oferta2.registrado_por == admin2


@pytest.mark.unit
@pytest.mark.finance
class TestBusinessLogicFinance(TestCase):
    """Testes para lógica de negócio financeira"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123",
            is_admin=True
        )
    
    def test_oferta_distribution_sum(self):
        """Testa que soma das distribuições não excede valor da oferta"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            registrado_por=self.admin
        )
        
        ong1 = ONG.objects.create(nome="ONG 1", cnpj="11.111.111/0001-11")
        ong2 = ONG.objects.create(nome="ONG 2", cnpj="22.222.222/0001-22")
        
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong1,
            valor=Decimal("400.00"),
            destino="ONG 1"
        )
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong2,
            valor=Decimal("600.00"),
            destino="ONG 2"
        )
        
        total_distribuido = sum(d.valor for d in oferta.distribuicoes.all())
        assert total_distribuido == Decimal("1000.00")
        assert total_distribuido <= oferta.valor


@pytest.mark.unit
@pytest.mark.finance
class TestTransacao(TestCase):
    """Testes para o modelo Transacao"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_transacao_entrada_creation(self):
        """Testa criação de transação de entrada"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.tipo == Transacao.ENTRADA
        assert transacao.valor == Decimal("500.00")
        assert transacao.categoria == "Dízimo"
    
    def test_transacao_saida_creation(self):
        """Testa criação de transação de saída"""
        transacao = Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa",
            valor=Decimal("100.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.tipo == Transacao.SAIDA
        assert transacao.valor == Decimal("100.00")
    
    def test_transacao_has_timestamps(self):
        """Testa que transação tem timestamps"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Oferta",
            valor=Decimal("200.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.created_at is not None
        assert transacao.updated_at is not None
        assert transacao.is_active is True
    
    def test_transacao_soft_delete(self):
        """Testa soft delete de transação"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("300.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        transacao.delete()
        
        assert transacao.deleted_at is not None
        assert transacao.is_active is False
        
        recuperada = Transacao.objects.filter(id=transacao.id).first()
        assert recuperada is None
    
    def test_transacao_with_metodo_pagamento(self):
        """Testa transação com método de pagamento"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            metodo_pagamento="PIX",
            registrado_por=self.admin
        )
        
        assert transacao.metodo_pagamento == "PIX"
    
    def test_transacao_with_observacoes(self):
        """Testa transação com observações"""
        obs = "Recebimento de dízimo do domingo"
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            observacoes=obs,
            registrado_por=self.admin
        )
        
        assert transacao.observacoes == obs
    
    def test_multiple_transacoes_entrada(self):
        """Testa múltiplas transações de entrada"""
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Oferta",
            valor=Decimal("300.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        entradas = Transacao.objects.filter(tipo=Transacao.ENTRADA)
        assert entradas.count() == 2
    
    def test_transacao_valor_positivo(self):
        """Testa que valor é positivo"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.valor > 0
    
    def test_transacao_entrada_saida_filter(self):
        """Testa filtro por tipo de transação"""
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa",
            valor=Decimal("100.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        entradas = Transacao.objects.filter(tipo=Transacao.ENTRADA).count()
        saidas = Transacao.objects.filter(tipo=Transacao.SAIDA).count()
        
        assert entradas == 1
        assert saidas == 1
    
    def test_transacao_update_valor(self):
        """Testa atualização de valor"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        novo_valor = Decimal("600.00")
        transacao.valor = novo_valor
        transacao.save()
        
        t_atualizada = Transacao.objects.get(id=transacao.id)
        assert t_atualizada.valor == novo_valor
    
    def test_transacao_update_categoria(self):
        """Testa atualização de categoria"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        nova_categoria = "Oferta Especial"
        transacao.categoria = nova_categoria
        transacao.save()
        
        t_atualizada = Transacao.objects.get(id=transacao.id)
        assert t_atualizada.categoria == nova_categoria


@pytest.mark.unit
@pytest.mark.finance
class TestTransacaoFinancial(TestCase):
    """Testes de análise financeira de transações"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_total_entradas(self):
        """Testa soma de transações de entrada"""
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Oferta",
            valor=Decimal("300.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        total = sum(t.valor for t in Transacao.objects.filter(tipo=Transacao.ENTRADA))
        assert total == Decimal("800.00")
    
    def test_total_saidas(self):
        """Testa soma de transações de saída"""
        Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa 1",
            valor=Decimal("100.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa 2",
            valor=Decimal("50.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        total = sum(t.valor for t in Transacao.objects.filter(tipo=Transacao.SAIDA))
        assert total == Decimal("150.00")
    
    def test_saldo_final(self):
        """Testa cálculo de saldo final"""
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("1000.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa",
            valor=Decimal("300.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        entradas = sum(t.valor for t in Transacao.objects.filter(tipo=Transacao.ENTRADA))
        saidas = sum(t.valor for t in Transacao.objects.filter(tipo=Transacao.SAIDA))
        saldo = entradas - saidas
        
        assert saldo == Decimal("700.00")
    
    def test_transacao_by_metodo_pagamento(self):
        """Testa agrupamento por método de pagamento"""
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            metodo_pagamento="PIX",
            registrado_por=self.admin
        )
        Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("300.00"),
            data=timezone.now().date(),
            metodo_pagamento="Dinheiro",
            registrado_por=self.admin
        )
        
        pix_count = Transacao.objects.filter(metodo_pagamento="PIX").count()
        dinheiro_count = Transacao.objects.filter(metodo_pagamento="Dinheiro").count()
        
        assert pix_count == 1
        assert dinheiro_count == 1
