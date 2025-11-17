import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app_alfa.models import Membro
from django.contrib.auth.hashers import make_password


class MembroLoginSeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_membro()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @classmethod
    def create_test_membro(cls):
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

    def test_login_membro_via_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
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
