"""Создание браузера Chrome через Selenium WebDriver и webdriver-manager."""
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome(headless: bool = False) -> webdriver.Chrome:
    """Запускает Chrome. ChromeDriver нужной версии скачивает и кэширует webdriver-manager."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--lang=ru")
    if os.getenv("CI"):  # GitHub Actions: у Chrome на сервере нет песочницы и мало разделяемой памяти
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
