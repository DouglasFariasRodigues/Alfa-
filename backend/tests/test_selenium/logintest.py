import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import django
from django.conf import settings

# Configurar Django
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
    django.setup()

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.models import User
from app_alfa.models import Admin, Membro
from django.contrib.auth.hashers import make_password


class LoginSeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_users()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @classmethod
    def create_test_users(cls):
        # Criar admin de teste
        admin_email = 'testadmin@example.com'
        admin_password = 'testpassword123'

        user, created = User.objects.get_or_create(
            username=admin_email,
            defaults={'email': admin_email, 'is_staff': True}
        )

        admin, created = Admin.objects.get_or_create(
            email=admin_email,
            defaults={
                'nome': 'Test Admin',
                'telefone': '(11) 99999-9999',
                'senha': make_password(admin_password),
                'cargo': None,
                'is_admin': True
            }
        )
        if not created:
            admin.senha = make_password(admin_password)
            admin.save()

        # Criar membro de teste
        membro_email = 'testmembro@example.com'
        membro_password = 'testpassword123'

        membro, created = Membro.objects.get_or_create(
            email=membro_email,
            defaults={
                'nome': 'Test Membro',
                'cpf': '12345678901',
                'telefone': '(11) 99999-9999',
                'senha': make_password(membro_password),
                'status': 'ativo',
                'cargo': None
            }
        )
        if not created:
            membro.senha = make_password(membro_password)
            membro.save()

    def test_login_admin_via_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(5)

        try:
            driver.get('http://localhost:8080/login')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            time.sleep(2)

            email_input = driver.find_element(By.ID, 'email')
            email_input.clear()
            for char in 'testadmin@example.com':
                email_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)

            senha_input = driver.find_element(By.ID, 'senha')
            senha_input.clear()
            for char in 'testpassword123':
                senha_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)

            login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            time.sleep(2)

            WebDriverWait(driver, 15).until(
                lambda driver: 'login' not in driver.current_url
            )

            self.assertNotIn('login', driver.current_url)

            time.sleep(2)

            token = driver.execute_script("return localStorage.getItem('access_token');")
            self.assertIsNotNone(token, "Token de acesso não foi encontrado no localStorage")

        finally:
            driver.quit()

    def test_login_membro_via_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)

        try:
            driver.get('http://localhost:8080/login')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            time.sleep(2)

            try:
                membro_tab = driver.find_element(By.XPATH, "//button[contains(text(), 'Membro')]")
            except:
                try:
                    membro_tab = driver.find_element(By.XPATH, "//button[contains(., 'Membro')]")
                except:
                    try:
                        membro_tab = driver.find_element(By.CSS_SELECTOR, '[value="membro"]')
                    except:
                        tabs = driver.find_elements(By.CSS_SELECTOR, 'button[data-radix-collection-item]')
                        for tab in tabs:
                            if 'Membro' in tab.text or 'membro' in tab.get_attribute('value').lower():
                                membro_tab = tab
                                break
                        else:
                            raise Exception("Aba Membro não encontrada")

            membro_tab.click()
            time.sleep(2)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'email-membro'))
            )
            time.sleep(1)

            email_input = driver.find_element(By.ID, 'email-membro')
            email_input.clear()
            for char in 'testmembro@example.com':
                email_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)

            senha_input = driver.find_element(By.ID, 'senha-membro')
            senha_input.clear()
            for char in 'testpassword123':
                senha_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)

            try:
                login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]:not([disabled])')
                login_button.click()
            except:
                login_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')
                if login_buttons:
                    login_buttons[0].click()
                else:
                    raise Exception("Botão de login não encontrado")
            time.sleep(2)

            WebDriverWait(driver, 15).until(
                lambda driver: 'login' not in driver.current_url
            )

            self.assertNotIn('login', driver.current_url)

            time.sleep(2)

            token = driver.execute_script("return localStorage.getItem('access_token');")
            self.assertIsNotNone(token, "Token de acesso não foi encontrado no localStorage")

        finally:
            driver.quit()


if __name__ == '__main__':
    unittest.main()