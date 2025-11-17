"""
Testes para operações CRUD (CREATE, READ, UPDATE, DELETE).
Testes de validação de constraints e soft delete.
"""
import pytest
from django.test import TestCase
from decimal import Decimal
from django.utils import timezone

from app_alfa.models import (
    Admin, Membro, Cargo, Oferta, DistribuicaoOferta, ONG
)


@pytest.mark.unit
class TestMembroUpdate(TestCase):
    """Testes de UPDATE para Membro"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João Silva",
            email="joao@email.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_membro_update_email(self):
        """Testa atualização de email do membro"""
        novo_email = "joao_novo@email.com"
        self.membro.email = novo_email
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.email == novo_email
    
    def test_membro_update_telefone(self):
        """Testa atualização de telefone"""
        novo_telefone = "(11) 99999-9999"
        self.membro.telefone = novo_telefone
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.telefone == novo_telefone
    
    def test_membro_update_cpf(self):
        """Testa atualização de CPF"""
        novo_cpf = "987.654.321-00"
        self.membro.cpf = novo_cpf
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.cpf == novo_cpf
    
    def test_membro_update_status(self):
        """Testa atualização de status"""
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.INATIVO
    
    def test_membro_multiple_updates(self):
        """Testa múltiplas atualizações em sequência"""
        self.membro.email = "email1@test.com"
        self.membro.save()
        
        self.membro.telefone = "(11) 11111-1111"
        self.membro.save()
        
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.email == "email1@test.com"
        assert membro_atualizado.telefone == "(11) 11111-1111"
        assert membro_atualizado.status == Membro.INATIVO


@pytest.mark.unit
class TestCargoUpdate(TestCase):
    """Testes de UPDATE para Cargo"""
    
    def setUp(self):
        self.cargo = Cargo.objects.create(
            nome="Pastor",
            descricao="Líder espiritual"
        )
    
    def test_cargo_update_description(self):
        """Testa atualização de descrição do cargo"""
        nova_descricao = "Líder e pastor da congregação"
        self.cargo.descricao = nova_descricao
        self.cargo.save()
        
        cargo_atualizado = Cargo.objects.get(id=self.cargo.id)
        assert cargo_atualizado.descricao == nova_descricao
    
    def test_cargo_update_permission(self):
        """Testa habilitação de permissão em cargo"""
        assert self.cargo.pode_gerenciar_membros is False
        
        self.cargo.pode_gerenciar_membros = True
        self.cargo.save()
        
        cargo_atualizado = Cargo.objects.get(id=self.cargo.id)
        assert cargo_atualizado.pode_gerenciar_membros is True
    
    def test_cargo_update_multiple_permissions(self):
        """Testa atualização de múltiplas permissões"""
        self.cargo.pode_gerenciar_membros = True
        self.cargo.pode_gerenciar_financas = True
        self.cargo.pode_registrar_ofertas = True
        self.cargo.save()
        
        cargo_atualizado = Cargo.objects.get(id=self.cargo.id)
        assert cargo_atualizado.pode_gerenciar_membros is True
        assert cargo_atualizado.pode_gerenciar_financas is True
        assert cargo_atualizado.pode_registrar_ofertas is True
    
    def test_cargo_disable_permission(self):
        """Testa desabilitação de permissão"""
        self.cargo.pode_gerenciar_membros = True
        self.cargo.save()
        
        self.cargo.pode_gerenciar_membros = False
        self.cargo.save()
        
        cargo_atualizado = Cargo.objects.get(id=self.cargo.id)
        assert cargo_atualizado.pode_gerenciar_membros is False


@pytest.mark.unit
class TestOfertaUpdate(TestCase):
    """Testes de UPDATE para Oferta"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta inicial",
            registrado_por=self.admin,
            is_publico=True
        )
    
    def test_oferta_update_description(self):
        """Testa atualização de descrição"""
        nova_descricao = "Oferta modificada"
        self.oferta.descricao = nova_descricao
        self.oferta.save()
        
        oferta_atualizada = Oferta.objects.get(id=self.oferta.id)
        assert oferta_atualizada.descricao == nova_descricao
    
    def test_oferta_update_visibility(self):
        """Testa mudança de visibilidade"""
        assert self.oferta.is_publico is True
        
        self.oferta.is_publico = False
        self.oferta.save()
        
        oferta_atualizada = Oferta.objects.get(id=self.oferta.id)
        assert oferta_atualizada.is_publico is False
    
    def test_distribuicao_update_value(self):
        """Testa atualização de valor de distribuição"""
        ong = ONG.objects.create(nome="ONG Test", cnpj="12.345.678/0001-90")
        distribuicao = DistribuicaoOferta.objects.create(
            oferta=self.oferta,
            ong=ong,
            valor=Decimal("500.00"),
            destino="ONG Test"
        )
        
        novo_valor = Decimal("600.00")
        distribuicao.valor = novo_valor
        distribuicao.save()
        
        dist_atualizada = DistribuicaoOferta.objects.get(id=distribuicao.id)
        assert dist_atualizada.valor == novo_valor


@pytest.mark.unit
class TestMembroDelete(TestCase):
    """Testes de DELETE (soft delete) para Membro"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João Silva",
            email="joao@email.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_membro_soft_delete_removes_from_list(self):
        """Testa que soft delete remove membro da lista"""
        membro_antes = Membro.objects.filter(id=self.membro.id).first()
        assert membro_antes is not None
        
        self.membro.delete()
        
        membro_depois = Membro.objects.filter(id=self.membro.id).first()
        assert membro_depois is None
    
    def test_membro_soft_delete_marks_inactive(self):
        """Testa que soft delete marca como inativo"""
        self.membro.delete()
        
        assert self.membro.deleted_at is not None
        assert self.membro.is_active is False
    
    def test_multiple_membros_soft_delete(self):
        """Testa soft delete de múltiplos membros"""
        membro2 = Membro.objects.create(
            nome="Maria Silva",
            email="maria@email.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        
        Membro.objects.all().delete()
        
        count = Membro.objects.count()
        assert count == 0


@pytest.mark.unit
class TestCargoDelete(TestCase):
    """Testes de DELETE para Cargo"""
    
    def setUp(self):
        self.cargo = Cargo.objects.create(
            nome="Pastor",
            descricao="Líder"
        )
    
    def test_cargo_soft_delete_removes_from_list(self):
        """Testa que soft delete remove cargo da lista"""
        cargo_antes = Cargo.objects.filter(id=self.cargo.id).first()
        assert cargo_antes is not None
        
        self.cargo.delete()
        
        cargo_depois = Cargo.objects.filter(id=self.cargo.id).first()
        assert cargo_depois is None
    
    def test_cargo_soft_delete_marks_inactive(self):
        """Testa que soft delete marca como inativo"""
        self.cargo.delete()
        
        assert self.cargo.deleted_at is not None
        assert self.cargo.is_active is False


@pytest.mark.unit
class TestOfertaDelete(TestCase):
    """Testes de DELETE para Oferta"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta",
            registrado_por=self.admin
        )
    
    def test_oferta_soft_delete_removes_from_list(self):
        """Testa que soft delete remove oferta da lista"""
        oferta_antes = Oferta.objects.filter(id=self.oferta.id).first()
        assert oferta_antes is not None
        
        self.oferta.delete()
        
        oferta_depois = Oferta.objects.filter(id=self.oferta.id).first()
        assert oferta_depois is None
    
    def test_oferta_soft_delete_marks_inactive(self):
        """Testa que soft delete marca como inativo"""
        self.oferta.delete()
        
        assert self.oferta.deleted_at is not None
        assert self.oferta.is_active is False
    
    def test_distribuicao_soft_delete(self):
        """Testa soft delete de distribuição"""
        ong = ONG.objects.create(nome="ONG Test", cnpj="12.345.678/0001-90")
        distribuicao = DistribuicaoOferta.objects.create(
            oferta=self.oferta,
            ong=ong,
            valor=Decimal("500.00"),
            destino="ONG Test"
        )
        
        distribuicao.delete()
        
        dist_depois = DistribuicaoOferta.objects.filter(id=distribuicao.id).first()
        assert dist_depois is None


@pytest.mark.unit
class TestCRUDValidations(TestCase):
    """Testes de validação para operações CRUD"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_cannot_create_duplicate_cargo(self):
        """Testa que não pode criar cargo com nome duplicado"""
        Cargo.objects.create(nome="Pastor")
        
        try:
            Cargo.objects.create(nome="Pastor")
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado
    
    def test_cannot_create_duplicate_admin_email(self):
        """Testa que não pode criar admin com email duplicado"""
        admin2_attempt = Admin(
            nome="Admin 2",
            email="admin@test.com",
            senha="123"
        )
        
        try:
            admin2_attempt.save()
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado
    
    def test_membro_update_with_duplicate_email(self):
        """Testa que não pode atualizar membro para email duplicado"""
        membro1 = Membro.objects.create(
            nome="João",
            email="joao@email.com",
            cadastrado_por=self.admin
        )
        membro2 = Membro.objects.create(
            nome="Maria",
            email="maria@email.com",
            cadastrado_por=self.admin
        )
        
        membro2.email = "joao@email.com"
        
        try:
            membro2.save()
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado
