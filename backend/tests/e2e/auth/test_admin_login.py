"""
Testes End-to-End com Selenium para autenticação.
Testa o fluxo completo de login na interface.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.hashers import make_password
from app_alfa.models import Admin, Membro


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.skip(reason="Requer ChromeDriver e configuração de ambiente")
class TestAdminLoginE2E:
    """Testes End-to-End para login de Admin"""
    
    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Preparar dados para E2E"""
        self.admin = Admin.objects.create(
            nome="Test Admin",
            email="testadmin@example.com",
            senha=make_password("testpassword123")
        )
    
    def test_admin_login_successful(self, selenium_driver, base_url):
        """Testa login bem-sucedido de admin"""
        selenium_driver.get(f"{base_url}/login")
        
        # Aguardar campo de email
        WebDriverWait(selenium_driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        
        # Preencher email
        email_input = selenium_driver.find_element(By.ID, "email")
        email_input.send_keys("testadmin@example.com")
        
        # Preencher senha
        senha_input = selenium_driver.find_element(By.ID, "senha")
        senha_input.send_keys("testpassword123")
        
        # Clicar botão login
        login_button = selenium_driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        )
        login_button.click()
        
        # Verificar redirecionamento
        WebDriverWait(selenium_driver, 15).until(
            lambda driver: "login" not in driver.current_url
        )
        
        assert "login" not in selenium_driver.current_url
    
    def test_admin_login_invalid_password(self, selenium_driver, base_url):
        """Testa login com senha incorreta"""
        selenium_driver.get(f"{base_url}/login")
        
        WebDriverWait(selenium_driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        
        email_input = selenium_driver.find_element(By.ID, "email")
        email_input.send_keys("testadmin@example.com")
        
        senha_input = selenium_driver.find_element(By.ID, "senha")
        senha_input.send_keys("wrongpassword")
        
        login_button = selenium_driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        )
        login_button.click()
        
        # Deve permanecer na página de login
        assert selenium_driver.current_url.endswith("/login")


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.skip(reason="Requer ChromeDriver e configuração de ambiente")
class TestMembroLoginE2E:
    """Testes End-to-End para login de Membro"""
    
    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Preparar dados para E2E"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="Test Membro",
            email="testmembro@example.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin,
            senha=make_password("testpassword123")
        )
    
    def test_membro_login_successful(self, selenium_driver, base_url):
        """Testa login bem-sucedido de membro"""
        selenium_driver.get(f"{base_url}/login")
        
        # Aguardar e clicar aba Membro
        WebDriverWait(selenium_driver, 10).until(
            EC.presence_of_element_located((By.ID, "email-membro"))
        )
        
        # Preencher credenciais de membro
        email_input = selenium_driver.find_element(By.ID, "email-membro")
        email_input.send_keys("testmembro@example.com")
        
        senha_input = selenium_driver.find_element(By.ID, "senha-membro")
        senha_input.send_keys("testpassword123")
        
        # Encontrar e clicar botão de login para membro
        login_button = selenium_driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        )
        login_button.click()
        
        # Verificar redirecionamento
        WebDriverWait(selenium_driver, 15).until(
            lambda driver: "login" not in driver.current_url
        )
        
        assert "login" not in selenium_driver.current_url
