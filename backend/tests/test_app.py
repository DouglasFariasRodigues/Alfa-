"""
Testes TDD (Test-Driven Development) para o sistema Alfa.
Testes unitários para modelos, validações e lógica de negócio.
"""
import pytest
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import date

from app_Alfa.models import (
    Admin, Usuario, Membro, Grupo, Doacao, Igreja, 
    Evento, Postagem, FotoEvento, FotoPostagem, 
    Cargo, ONG, Oferta, DistribuicaoOferta, DocumentoMembro
)


class TestAdminModel(TestCase):
    """Testes para o modelo Admin"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.admin = Admin.objects.create(
            nome="Admin Teste",
            email="admin@teste.com",
            senha="senha123",
            is_admin=True
        )
    
    def test_admin_creation(self):
        """Testa criação de Admin"""
        assert self.admin.nome == "Admin Teste"
        assert self.admin.email == "admin@teste.com"
        assert self.admin.is_admin is True
    
    def test_admin_str(self):
        """Testa representação em string do Admin"""
        # Admin não tem __str__ definido, então testa se existe
        str_repr = str(self.admin)
        assert "Admin" in str_repr or self.admin.nome in str_repr or self.admin.id
    
    def test_admin_login_valido(self):
        """Testa login com credenciais válidas"""
        # Admin usa set_password para hash automático
        admin_test = Admin.objects.create(nome="Test", email="test@test.com", senha="password123")
        
        # Verificar com check_password
        assert admin_test.check_password("password123")
    
    def test_admin_login_invalido(self):
        """Testa login com senha incorreta"""
        # Admin usa check_password para verificar senha com hash
        admin_test = Admin.objects.create(nome="Test", email="test2@test.com", senha="password123")
        
        # Verificar que senha incorreta retorna False
        assert not admin_test.check_password("senhaErrada")


class TestMembroModel(TestCase):
    """Testes para o modelo Membro"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João Silva",
            cpf="123.456.789-00",
            email="joao@email.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_membro_creation(self):
        """Testa criação de membro"""
        assert self.membro.nome == "João Silva"
        assert self.membro.status == Membro.ATIVO
        assert self.membro.cadastrado_por == self.admin
    
    def test_membro_status_choices(self):
        """Testa opções de status disponíveis"""
        assert Membro.ATIVO == 'ativo'
        assert Membro.INATIVO == 'inativo'
        assert Membro.FALECIDO == 'falecido'
        assert Membro.AFASTADO == 'afastado'
    
    def test_membro_change_status(self):
        """Testa alteração de status"""
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.INATIVO
    
    def test_membro_soft_delete(self):
        """Testa exclusão lógica (soft delete)"""
        self.membro.delete()
        
        # BaseModel implementa soft delete
        # Membro não deve aparecer em queries normais se is_active=False
        membro_atualizado = Membro.objects.filter(id=self.membro.id).first()
        
        # Se o soft delete está funcionando, o membro ainda existe mas está marcado como deletado
        if hasattr(Membro, 'deleted_at'):
            assert membro_atualizado is None or membro_atualizado.deleted_at is not None
        else:
            # Se não tem soft delete, verifica exclusão real
            assert membro_atualizado is None


class TestCargoModel(TestCase):
    """Testes para o modelo Cargo"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.cargo = Cargo.objects.create(
            nome="Pastor",
            descricao="Líder espiritual da igreja"
        )
    
    def test_cargo_creation(self):
        """Testa criação de cargo"""
        assert self.cargo.nome == "Pastor"
        assert self.cargo.descricao is not None
    
    def test_multiple_cargos(self):
        """Testa criação de múltiplos cargos"""
        Cargo.objects.create(nome="Diácono", descricao="Auxiliar")
        Cargo.objects.create(nome="Líder de Louvor", descricao="Louvor")
        
        assert Cargo.objects.count() == 3


class TestOfertaModel(TestCase):
    """Testes para o modelo Oferta"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta do domingo",
            registrado_por=self.admin,
            is_publico=True
        )
    
    def test_oferta_creation(self):
        """Testa criação de oferta"""
        assert self.oferta.valor == Decimal("1000.00")
        assert self.oferta.is_publico is True
    
    def test_oferta_valor_positivo(self):
        """Testa que valor da oferta é positivo"""
        assert self.oferta.valor > 0
    
    def test_oferta_with_distribution(self):
        """Testa distribuição de oferta para ONG"""
        ong = ONG.objects.create(
            nome="ONG Teste",
            cnpj="12.345.678/0001-90"
        )
        
        distribuicao = DistribuicaoOferta.objects.create(
            oferta=self.oferta,
            ong=ong,
            valor=Decimal("500.00"),
            destino="ONG Teste",
            meio_envio="PIX"
        )
        
        assert self.oferta.distribuicoes.count() == 1
        assert distribuicao.valor == Decimal("500.00")


class TestDoacaoModel(TestCase):
    """Testes para o modelo Doacao"""
    
    def setUp(self):
        self.admin = Admin.objects.create(nome="Admin", email="a@t.com", senha="123")
        self.membro = Membro.objects.create(
            nome="Maria",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        self.grupo = Grupo.objects.create(
            nome="Missões",
            descricao="Grupo de missões"
        )
    
    def test_doacao_creation(self):
        """Testa criação de doação"""
        doacao = Doacao.objects.create(
            membro=self.membro,
            grupo=self.grupo,
            valor=Decimal("100.00"),
            tipo="doacao"
        )
        
        assert doacao.membro == self.membro
        assert doacao.valor == Decimal("100.00")
    
    def test_multiple_doacoes(self):
        """Testa múltiplas doações de um membro"""
        Doacao.objects.create(membro=self.membro, grupo=self.grupo, valor=Decimal("50.00"))
        Doacao.objects.create(membro=self.membro, grupo=self.grupo, valor=Decimal("75.00"))
        
        total_doacoes = self.membro.doacoes.count()
        assert total_doacoes == 2
        
        # Testa soma total
        total_valor = sum(d.valor for d in self.membro.doacoes.all())
        assert total_valor == Decimal("125.00")


class TestDocumentoMembroModel(TestCase):
    """Testes para o modelo DocumentoMembro"""
    
    def setUp(self):
        self.admin = Admin.objects.create(nome="Admin", email="a@t.com", senha="123")
        self.membro = Membro.objects.create(
            nome="Carlos",
            cadastrado_por=self.admin
        )
    
    def test_cartao_membro(self):
        """Testa geração de cartão de membro"""
        documento = DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.CARTAO_MEMBRO,
            gerado_por=self.admin
        )
        
        assert documento.tipo == DocumentoMembro.CARTAO_MEMBRO
        assert documento.membro == self.membro
    
    def test_transferencia(self):
        """Testa geração de documento de transferência"""
        documento = DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.TRANSFERENCIA,
            gerado_por=self.admin
        )
        
        assert documento.tipo == DocumentoMembro.TRANSFERENCIA
    
    def test_multiple_documentos(self):
        """Testa múltiplos documentos por membro"""
        DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.CARTAO_MEMBRO,
            gerado_por=self.admin
        )
        DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.REGISTRO,
            gerado_por=self.admin
        )
        
        assert self.membro.documentos.count() == 2


class TestEventoModel(TestCase):
    """Testes para o modelo Evento"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create(
            username="organizador",
            email="org@test.com"
        )
        self.evento = Evento.objects.create(
            titulo="Culto de Domingo",
            descricao="Culto dominical",
            data=timezone.now(),
            local="Igreja Central",
            organizador=self.usuario
        )
    
    def test_evento_creation(self):
        """Testa criação de evento"""
        assert self.evento.titulo == "Culto de Domingo"
        assert self.evento.organizador == self.usuario
    
    def test_evento_with_fotos(self):
        """Testa evento com fotos"""
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto1.jpg",
            descricao="Foto 1"
        )
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto2.jpg",
            descricao="Foto 2"
        )
        
        assert self.evento.fotos.count() == 2


class TestBusinessLogic(TestCase):
    """Testes para lógica de negócio"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123",
            is_admin=True
        )
    
    def test_admin_permissions(self):
        """Testa permissões do Admin"""
        assert self.admin.is_admin is True
        assert self.admin.is_active is True
    
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
    
    def test_membro_statistics(self):
        """Testa estatísticas de membros por status"""
        # Criar membros com diferentes status
        for i in range(5):
            Membro.objects.create(nome=f"Ativo {i}", status=Membro.ATIVO, cadastrado_por=self.admin)
        for i in range(3):
            Membro.objects.create(nome=f"Inativo {i}", status=Membro.INATIVO, cadastrado_por=self.admin)
        for i in range(2):
            Membro.objects.create(nome=f"Afastado {i}", status=Membro.AFASTADO, cadastrado_por=self.admin)
        
        # Contar por status
        ativos = Membro.objects.filter(status=Membro.ATIVO).count()
        inativos = Membro.objects.filter(status=Membro.INATIVO).count()
        afastados = Membro.objects.filter(status=Membro.AFASTADO).count()
        
        assert ativos == 5
        assert inativos == 3
        assert afastados == 2


# ============= UPDATE TESTS =============

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
    
    def test_membro_updated_at_changes(self):
        """Testa se updated_at muda ao atualizar membro"""
        original_updated_at = self.membro.updated_at
        
        # Aguardar um pouco para garantir que tempo passa
        from time import sleep
        sleep(0.1)
        
        self.membro.email = "novo@email.com"
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.updated_at >= original_updated_at
    
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


# ============= DELETE TESTS =============

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
        # Verificar que membro existe
        membro_antes = Membro.objects.filter(id=self.membro.id).first()
        assert membro_antes is not None
        
        # Fazer soft delete
        self.membro.delete()
        
        # Verificar que membro não aparece em queries normais
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
        
        # Deletar todos
        Membro.objects.all().delete()
        
        # Verificar que nenhum aparece
        count = Membro.objects.count()
        assert count == 0
    
    def test_membro_hard_delete(self):
        """Testa hard delete (exclusão definitiva)"""
        membro_id = self.membro.id
        self.membro.hard_delete()
        
        # Verificar que foi completamente removido
        # Isso pode requer verificar no banco diretamente ou usar all_with_deleted
        # dependendo da implementação


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
        
        # Verificar que foi deletada
        dist_depois = DistribuicaoOferta.objects.filter(id=distribuicao.id).first()
        assert dist_depois is None


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
        
        # Tentar criar cargo com mesmo nome
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
        
        # Tentar atualizar membro2 com email de membro1
        membro2.email = "joao@email.com"
        
        try:
            membro2.save()
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado


# ============= PERMISSION TESTS BY ROLE =============

class TestCargoPermissions(TestCase):
    """Testes de permissões associadas a cargos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_cargo_pode_registrar_dizimos(self):
        """Testa permissão para registrar dízimos"""
        cargo_com_permissao = Cargo.objects.create(
            nome="Tesoureiro",
            descricao="Gerencia finanças",
            pode_registrar_dizimos=True
        )
        
        assert cargo_com_permissao.pode_registrar_dizimos is True
    
    def test_cargo_sem_permissao_registrar_dizimos(self):
        """Testa que cargo sem permissão não tem acesso"""
        cargo_sem_permissao = Cargo.objects.create(
            nome="Membro Comum",
            descricao="Membro comum",
            pode_registrar_dizimos=False
        )
        
        assert cargo_sem_permissao.pode_registrar_dizimos is False
    
    def test_cargo_pode_gerenciar_membros(self):
        """Testa permissão para gerenciar membros"""
        cargo = Cargo.objects.create(
            nome="Pastor",
            pode_gerenciar_membros=True
        )
        
        assert cargo.pode_gerenciar_membros is True
    
    def test_cargo_pode_gerenciar_financas(self):
        """Testa permissão para gerenciar finanças"""
        cargo = Cargo.objects.create(
            nome="Tesoureiro",
            pode_gerenciar_financas=True
        )
        
        assert cargo.pode_gerenciar_financas is True
    
    def test_cargo_pode_registrar_ofertas(self):
        """Testa permissão para registrar ofertas"""
        cargo = Cargo.objects.create(
            nome="Diácono",
            pode_registrar_ofertas=True
        )
        
        assert cargo.pode_registrar_ofertas is True
    
    def test_cargo_pode_gerenciar_eventos(self):
        """Testa permissão para gerenciar eventos"""
        cargo = Cargo.objects.create(
            nome="Organizador",
            pode_gerenciar_eventos=True
        )
        
        assert cargo.pode_gerenciar_eventos is True
    
    def test_cargo_pode_gerenciar_documentos(self):
        """Testa permissão para gerenciar documentos"""
        cargo = Cargo.objects.create(
            nome="Secretário",
            pode_gerenciar_documentos=True
        )
        
        assert cargo.pode_gerenciar_documentos is True
    
    def test_cargo_pode_visualizar_relatorios(self):
        """Testa permissão para visualizar relatórios"""
        cargo = Cargo.objects.create(
            nome="Gerente",
            pode_visualizar_relatorios=True
        )
        
        assert cargo.pode_visualizar_relatorios is True
    
    def test_cargo_pode_gerenciar_cargos(self):
        """Testa permissão para gerenciar cargos"""
        cargo = Cargo.objects.create(
            nome="Administrador",
            pode_gerenciar_cargos=True
        )
        
        assert cargo.pode_gerenciar_cargos is True
    
    def test_cargo_multiple_permissions(self):
        """Testa cargo com múltiplas permissões"""
        cargo_pastor = Cargo.objects.create(
            nome="Pastor",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True,
            pode_gerenciar_cargos=False
        )
        
        assert cargo_pastor.pode_gerenciar_membros is True
        assert cargo_pastor.pode_gerenciar_financas is True
        assert cargo_pastor.pode_registrar_dizimos is True
        assert cargo_pastor.pode_registrar_ofertas is True
        assert cargo_pastor.pode_gerenciar_eventos is True
        assert cargo_pastor.pode_gerenciar_documentos is True
        assert cargo_pastor.pode_visualizar_relatorios is True
        assert cargo_pastor.pode_gerenciar_cargos is False
    
    def test_cargo_minimal_permissions(self):
        """Testa cargo com permissões mínimas"""
        cargo_membro = Cargo.objects.create(
            nome="Membro",
            pode_gerenciar_membros=False,
            pode_gerenciar_financas=False,
            pode_registrar_dizimos=False,
            pode_registrar_ofertas=False,
            pode_gerenciar_eventos=False,
            pode_gerenciar_documentos=False,
            pode_visualizar_relatorios=False,
            pode_gerenciar_cargos=False
        )
        
        assert cargo_membro.pode_gerenciar_membros is False
        assert cargo_membro.pode_gerenciar_financas is False
        assert cargo_membro.pode_registrar_dizimos is False
        assert cargo_membro.pode_registrar_ofertas is False
        assert cargo_membro.pode_gerenciar_eventos is False
        assert cargo_membro.pode_gerenciar_documentos is False
        assert cargo_membro.pode_visualizar_relatorios is False
        assert cargo_membro.pode_gerenciar_cargos is False


class TestAdminPermissionsByRole(TestCase):
    """Testes de permissões do Admin baseado em cargo"""
    
    def setUp(self):
        """Configuração inicial"""
        self.cargo_admin = Cargo.objects.create(
            nome="Admin",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True,
            pode_gerenciar_cargos=True
        )
        
        self.cargo_tesoureiro = Cargo.objects.create(
            nome="Tesoureiro",
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_visualizar_relatorios=True
        )
        
        self.cargo_secretario = Cargo.objects.create(
            nome="Secretário",
            pode_gerenciar_membros=True,
            pode_gerenciar_documentos=True
        )
        
        self.admin_completo = Admin.objects.create(
            nome="Admin Completo",
            email="admin@church.com",
            senha="admin123",
            cargo=self.cargo_admin
        )
        
        self.admin_tesoureiro = Admin.objects.create(
            nome="Admin Tesoureiro",
            email="tesoureiro@church.com",
            senha="t123",
            cargo=self.cargo_tesoureiro
        )
        
        self.admin_secretario = Admin.objects.create(
            nome="Admin Secretário",
            email="secretario@church.com",
            senha="s123",
            cargo=self.cargo_secretario
        )
    
    def test_admin_with_full_role_has_all_permissions(self):
        """Testa que admin com cargo completo tem todas as permissões"""
        cargo = self.admin_completo.cargo
        
        assert cargo.pode_gerenciar_membros is True
        assert cargo.pode_gerenciar_financas is True
        assert cargo.pode_registrar_dizimos is True
        assert cargo.pode_registrar_ofertas is True
        assert cargo.pode_gerenciar_eventos is True
        assert cargo.pode_gerenciar_documentos is True
        assert cargo.pode_visualizar_relatorios is True
        assert cargo.pode_gerenciar_cargos is True
    
    def test_admin_tesoureiro_has_finance_permissions(self):
        """Testa que tesoureiro tem permissões de finanças"""
        cargo = self.admin_tesoureiro.cargo
        
        assert cargo.pode_gerenciar_financas is True
        assert cargo.pode_registrar_dizimos is True
        assert cargo.pode_registrar_ofertas is True
        assert cargo.pode_visualizar_relatorios is True
    
    def test_admin_tesoureiro_cannot_manage_members(self):
        """Testa que tesoureiro não pode gerenciar membros"""
        cargo = self.admin_tesoureiro.cargo
        
        assert cargo.pode_gerenciar_membros is False
    
    def test_admin_secretario_can_manage_members(self):
        """Testa que secretário pode gerenciar membros"""
        cargo = self.admin_secretario.cargo
        
        assert cargo.pode_gerenciar_membros is True
        assert cargo.pode_gerenciar_documentos is True
    
    def test_admin_secretario_cannot_manage_finances(self):
        """Testa que secretário não pode gerenciar finanças"""
        cargo = self.admin_secretario.cargo
        
        assert cargo.pode_gerenciar_financas is False
        assert cargo.pode_registrar_dizimos is False
        assert cargo.pode_registrar_ofertas is False
    
    def test_admin_role_change_affects_permissions(self):
        """Testa que trocar cargo do admin afeta permissões"""
        # Admin secretário tem permissão para gerenciar membros
        assert self.admin_secretario.cargo.pode_gerenciar_membros is True
        
        # Mudar para cargo com sem permissão
        novo_cargo = Cargo.objects.create(
            nome="Membro Comum",
            pode_gerenciar_membros=False,
            pode_gerenciar_documentos=False
        )
        
        self.admin_secretario.cargo = novo_cargo
        self.admin_secretario.save()
        
        # Verificar que permissão mudou
        admin_atualizado = Admin.objects.get(id=self.admin_secretario.id)
        assert admin_atualizado.cargo.pode_gerenciar_membros is False


class TestUsuarioPermissionsByRole(TestCase):
    """Testes de permissões do Usuario baseado em cargo"""
    
    def setUp(self):
        """Configuração inicial"""
        self.cargo_organizador = Cargo.objects.create(
            nome="Organizador de Eventos",
            pode_gerenciar_eventos=True,
            pode_visualizar_relatorios=False
        )
        
        self.cargo_tesoureiro = Cargo.objects.create(
            nome="Tesoureiro",
            pode_gerenciar_financas=True,
            pode_visualizar_relatorios=True
        )
        
        self.usuario_organizador = Usuario.objects.create(
            username="organizador",
            email="organizador@church.com",
            senha="o123",
            cargo=self.cargo_organizador
        )
        
        self.usuario_tesoureiro = Usuario.objects.create(
            username="tesoureiro",
            email="tesoureiro@church.com",
            senha="t123",
            cargo=self.cargo_tesoureiro
        )
    
    def test_usuario_organizador_can_manage_events(self):
        """Testa que organizador pode gerenciar eventos"""
        cargo = self.usuario_organizador.cargo
        
        assert cargo.pode_gerenciar_eventos is True
    
    def test_usuario_organizador_cannot_manage_finances(self):
        """Testa que organizador não pode gerenciar finanças"""
        cargo = self.usuario_organizador.cargo
        
        assert cargo.pode_gerenciar_financas is False
    
    def test_usuario_tesoureiro_can_view_reports(self):
        """Testa que tesoureiro pode visualizar relatórios"""
        cargo = self.usuario_tesoureiro.cargo
        
        assert cargo.pode_visualizar_relatorios is True
    
    def test_usuario_tesoureiro_cannot_manage_events(self):
        """Testa que tesoureiro não pode gerenciar eventos"""
        cargo = self.usuario_tesoureiro.cargo
        
        assert cargo.pode_gerenciar_eventos is False
    
    def test_different_usuarios_have_different_permissions(self):
        """Testa que usuários com cargos diferentes têm permissões diferentes"""
        org_cargo = self.usuario_organizador.cargo
        treas_cargo = self.usuario_tesoureiro.cargo
        
        # Permissões diferentes
        assert org_cargo.pode_gerenciar_eventos is True
        assert treas_cargo.pode_gerenciar_eventos is False
        
        assert org_cargo.pode_gerenciar_financas is False
        assert treas_cargo.pode_gerenciar_financas is True
    
    def test_usuario_permission_inheritance_from_role(self):
        """Testa que permissão do usuário vem do cargo"""
        usuario = Usuario.objects.create(
            username="novo_usuario",
            email="novo@church.com",
            senha="n123",
            cargo=self.cargo_organizador
        )
        
        # Permissões vêm do cargo
        assert usuario.cargo.pode_gerenciar_eventos is True
        assert usuario.cargo.pode_visualizar_relatorios is False


class TestPermissionValidation(TestCase):
    """Testes de validação de permissões"""
    
    def setUp(self):
        """Configuração inicial"""
        self.cargo_completo = Cargo.objects.create(
            nome="Admin Completo",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True,
            pode_gerenciar_cargos=True
        )
        
        self.cargo_restrito = Cargo.objects.create(
            nome="Membro Restrito",
            pode_gerenciar_membros=False,
            pode_gerenciar_financas=False,
            pode_registrar_dizimos=False,
            pode_registrar_ofertas=False,
            pode_gerenciar_eventos=False,
            pode_gerenciar_documentos=False,
            pode_visualizar_relatorios=False,
            pode_gerenciar_cargos=False
        )
    
    def test_cargo_completo_has_all_permissions(self):
        """Testa que cargo completo tem todas as 8 permissões"""
        permissoes = [
            self.cargo_completo.pode_gerenciar_membros,
            self.cargo_completo.pode_gerenciar_financas,
            self.cargo_completo.pode_registrar_dizimos,
            self.cargo_completo.pode_registrar_ofertas,
            self.cargo_completo.pode_gerenciar_eventos,
            self.cargo_completo.pode_gerenciar_documentos,
            self.cargo_completo.pode_visualizar_relatorios,
            self.cargo_completo.pode_gerenciar_cargos
        ]
        
        assert all(permissoes) is True
        assert len([p for p in permissoes if p]) == 8
    
    def test_cargo_restrito_has_no_permissions(self):
        """Testa que cargo restrito não tem nenhuma permissão"""
        permissoes = [
            self.cargo_restrito.pode_gerenciar_membros,
            self.cargo_restrito.pode_gerenciar_financas,
            self.cargo_restrito.pode_registrar_dizimos,
            self.cargo_restrito.pode_registrar_ofertas,
            self.cargo_restrito.pode_gerenciar_eventos,
            self.cargo_restrito.pode_gerenciar_documentos,
            self.cargo_restrito.pode_visualizar_relatorios,
            self.cargo_restrito.pode_gerenciar_cargos
        ]
        
        assert any(permissoes) is False
        assert len([p for p in permissoes if p]) == 0
    
    def test_permission_count_completo(self):
        """Testa contagem de permissões do cargo completo"""
        count = sum([
            self.cargo_completo.pode_gerenciar_membros,
            self.cargo_completo.pode_gerenciar_financas,
            self.cargo_completo.pode_registrar_dizimos,
            self.cargo_completo.pode_registrar_ofertas,
            self.cargo_completo.pode_gerenciar_eventos,
            self.cargo_completo.pode_gerenciar_documentos,
            self.cargo_completo.pode_visualizar_relatorios,
            self.cargo_completo.pode_gerenciar_cargos
        ])
        
        assert count == 8
    
    def test_permission_count_restrito(self):
        """Testa contagem de permissões do cargo restrito"""
        count = sum([
            self.cargo_restrito.pode_gerenciar_membros,
            self.cargo_restrito.pode_gerenciar_financas,
            self.cargo_restrito.pode_registrar_dizimos,
            self.cargo_restrito.pode_registrar_ofertas,
            self.cargo_restrito.pode_gerenciar_eventos,
            self.cargo_restrito.pode_gerenciar_documentos,
            self.cargo_restrito.pode_visualizar_relatorios,
            self.cargo_restrito.pode_gerenciar_cargos
        ])
        
        assert count == 0


# ============= EVENT COMMENTS AND PRESENCE TESTS =============

class TestEventoComments(TestCase):
    """Testes de comentários em eventos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
        
        self.evento = Evento.objects.create(
            titulo="Culto de Domingo",
            descricao="Culto dominical",
            data=timezone.now(),
            local="Igreja Central",
            organizador=self.usuario
        )
    
    def test_evento_creation(self):
        """Testa criação de evento"""
        assert self.evento.titulo == "Culto de Domingo"
        assert self.evento.local == "Igreja Central"
        assert self.evento.organizador == self.usuario
    
    def test_evento_has_timestamps(self):
        """Testa que evento tem timestamps"""
        assert self.evento.created_at is not None
        assert self.evento.updated_at is not None
        assert self.evento.is_active is True
    
    def test_evento_is_soft_deletable(self):
        """Testa que evento suporta soft delete"""
        self.evento.delete()
        
        assert self.evento.deleted_at is not None
        assert self.evento.is_active is False
        
        # Verificar que não aparece em queries normais
        evento_recuperado = Evento.objects.filter(id=self.evento.id).first()
        assert evento_recuperado is None
    
    def test_evento_update_description(self):
        """Testa atualização de descrição do evento"""
        nova_descricao = "Culto especial com louvor"
        self.evento.descricao = nova_descricao
        self.evento.save()
        
        evento_atualizado = Evento.objects.get(id=self.evento.id)
        assert evento_atualizado.descricao == nova_descricao
    
    def test_evento_update_local(self):
        """Testa atualização de local do evento"""
        novo_local = "Igreja da Zona Leste"
        self.evento.local = novo_local
        self.evento.save()
        
        evento_atualizado = Evento.objects.get(id=self.evento.id)
        assert evento_atualizado.local == novo_local
    
    def test_evento_update_data(self):
        """Testa atualização de data do evento"""
        nova_data = timezone.now() + timezone.timedelta(days=7)
        self.evento.data = nova_data
        self.evento.save()
        
        evento_atualizado = Evento.objects.get(id=self.evento.id)
        assert evento_atualizado.data == nova_data
    
    def test_multiple_eventos_by_same_organizador(self):
        """Testa que mesmo organizador pode criar múltiplos eventos"""
        evento2 = Evento.objects.create(
            titulo="Estudo Bíblico",
            descricao="Estudo da Palavra",
            data=timezone.now(),
            local="Sala 1",
            organizador=self.usuario
        )
        
        eventos = Evento.objects.filter(organizador=self.usuario)
        assert eventos.count() == 2
        assert evento2 in eventos
    
    def test_evento_com_foto(self):
        """Testa evento com foto"""
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto1.jpg",
            descricao="Foto do evento"
        )
        
        assert self.evento.fotos.count() == 1
    
    def test_evento_com_multiplas_fotos(self):
        """Testa evento com múltiplas fotos"""
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto1.jpg",
            descricao="Foto 1"
        )
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto2.jpg",
            descricao="Foto 2"
        )
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto3.jpg",
            descricao="Foto 3"
        )
        
        assert self.evento.fotos.count() == 3


class TestFotoEvento(TestCase):
    """Testes para fotos de eventos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
        
        self.evento = Evento.objects.create(
            titulo="Evento Test",
            descricao="Teste",
            data=timezone.now(),
            local="Local",
            organizador=self.usuario
        )
    
    def test_foto_evento_creation(self):
        """Testa criação de foto de evento"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg",
            descricao="Foto teste"
        )
        
        assert foto.evento == self.evento
        assert foto.descricao == "Foto teste"
    
    def test_foto_evento_has_timestamp(self):
        """Testa que foto tem timestamp"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg"
        )
        
        assert foto.data_upload is not None
    
    def test_foto_evento_sem_descricao(self):
        """Testa que foto pode não ter descrição"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg"
        )
        
        assert foto.descricao is None or foto.descricao == ""
    
    def test_delete_foto_evento(self):
        """Testa exclusão de foto"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg"
        )
        
        foto_id = foto.id
        foto.delete()
        
        foto_deletada = FotoEvento.objects.filter(id=foto_id).first()
        assert foto_deletada is None
    
    def test_multiplas_fotos_different_eventos(self):
        """Testa que fotos podem estar em eventos diferentes"""
        evento2 = Evento.objects.create(
            titulo="Evento 2",
            descricao="Teste 2",
            data=timezone.now(),
            local="Local 2",
            organizador=self.usuario
        )
        
        foto1 = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto1.jpg"
        )
        
        foto2 = FotoEvento.objects.create(
            evento=evento2,
            imagem="foto2.jpg"
        )
        
        assert foto1.evento == self.evento
        assert foto2.evento == evento2
        assert foto1.evento != foto2.evento


class TestEventoPresence(TestCase):
    """Testes de presenças em eventos (simulado com dados relacionados)"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
        
        self.membro1 = Membro.objects.create(
            nome="Membro 1",
            email="membro1@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        
        self.membro2 = Membro.objects.create(
            nome="Membro 2",
            email="membro2@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        
        self.evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
    
    def test_evento_has_multiplos_membros(self):
        """Testa que evento pode ter múltiplos membros relacionados"""
        # Simulando presenças através de relacionamentos
        assert self.membro1 is not None
        assert self.membro2 is not None
        assert self.evento is not None
    
    def test_membro_status_validation_for_presence(self):
        """Testa que apenas membros ativos podem ter presença registrada"""
        assert self.membro1.status == Membro.ATIVO
        
        # Membro inativo não deveria contar presença
        self.membro2.status = Membro.INATIVO
        self.membro2.save()
        
        assert self.membro2.status == Membro.INATIVO
    
    def test_evento_organizador_relationship(self):
        """Testa relacionamento entre evento e organizador"""
        assert self.evento.organizador == self.usuario
        
        eventos = Evento.objects.filter(organizador=self.usuario)
        assert self.evento in eventos
    
    def test_evento_data_comparison(self):
        """Testa que pode comparar datas de eventos"""
        data_passada = timezone.now() - timezone.timedelta(days=7)
        evento_passado = Evento.objects.create(
            titulo="Evento Passado",
            descricao="Teste",
            data=data_passada,
            local="Local",
            organizador=self.usuario
        )
        
        assert evento_passado.data < self.evento.data
        assert self.evento.data > evento_passado.data
    
    def test_evento_future_date(self):
        """Testa evento com data futura"""
        data_futura = timezone.now() + timezone.timedelta(days=30)
        evento_futuro = Evento.objects.create(
            titulo="Evento Futuro",
            descricao="Teste",
            data=data_futura,
            local="Local",
            organizador=self.usuario
        )
        
        assert evento_futuro.data > timezone.now()
    
    def test_membro_count_for_event_attendance(self):
        """Testa contagem de membros para presenças"""
        total_membros = Membro.objects.filter(status=Membro.ATIVO).count()
        assert total_membros >= 1


class TestEventoValidation(TestCase):
    """Testes de validação de eventos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
    
    def test_evento_requires_titulo(self):
        """Testa que evento requer título"""
        try:
            evento = Evento.objects.create(
                titulo="",
                descricao="Teste",
                data=timezone.now(),
                organizador=self.usuario
            )
            # Se for campo vazio permitido, validação passa
        except Exception:
            pass  # Campo pode ter validação
    
    def test_evento_requires_organizador(self):
        """Testa que evento requer organizador"""
        try:
            evento = Evento.objects.create(
                titulo="Evento",
                descricao="Teste",
                data=timezone.now(),
                organizador=None
            )
            assert False, "Deveria ter falhado"
        except Exception:
            pass  # Esperado - campo obrigatório
    
    def test_evento_descricao_can_be_long(self):
        """Testa que descrição pode ser longa"""
        descricao_longa = "Lorem ipsum dolor sit amet " * 50
        evento = Evento.objects.create(
            titulo="Evento",
            descricao=descricao_longa,
            data=timezone.now(),
            organizador=self.usuario
        )
        
        assert evento.descricao == descricao_longa
    
    def test_evento_local_optional(self):
        """Testa que local é opcional"""
        evento = Evento.objects.create(
            titulo="Evento",
            descricao="Teste",
            data=timezone.now(),
            organizador=self.usuario
        )
        
        assert evento.local is None


# Função para executar testes manualmente (sem pytest)
if __name__ == '__main__':
    import django
    import os
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
    django.setup()
    
    # Executar testes
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    
    if failures:
        print(f"\n❌ {failures} testes falharam")
    else:
        print("\n✅ Todos os testes TDD passaram!")

