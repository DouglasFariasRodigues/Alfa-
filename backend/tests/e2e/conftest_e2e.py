"""
Configuração para testes End-to-End com Selenium.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def selenium_driver():
    """Fornece um driver Selenium Chrome configurado."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


@pytest.fixture
def base_url(live_server):
    """URL base do servidor de testes."""
    return f"http://{live_server.host}:{live_server.port}"
