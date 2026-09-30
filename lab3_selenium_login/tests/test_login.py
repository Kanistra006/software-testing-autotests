"""Автотесты страницы входа стенда TaskFlow (Selenium WebDriver + pytest)."""
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Локаторы выбраны по результатам анализа селекторов (см. отчёт, раздел 3)
USERNAME = (By.ID, "username")
PASSWORD = (By.ID, "password")
SUBMIT = (By.CSS_SELECTOR, "#login-form button[type='submit']")  # id кнопки меняется при каждой загрузке
ERROR = (By.CSS_SELECTOR, "#login-form [role='alert']")           # у сообщения нет id
LOGOUT_NOTICE = (By.CSS_SELECTOR, "[data-role='logout-notice']")
LOGOUT = (By.ID, "logout")
CURRENT_USER = (By.ID, "current-user")

VALID_LOGIN = "student"
VALID_PASSWORD = "Test123!"
TIMEOUT = 5  # секунд; вход на стенде имитирует задержку сервера 0,7 с
ARTIFACTS = Path(__file__).parent.parent / "artifacts"


def open_login_page(driver, base_url):
    driver.get(f"{base_url}/login.html")
    WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located(USERNAME))


def fill_credentials(driver, username, password):
    driver.find_element(*USERNAME).send_keys(username)
    driver.find_element(*PASSWORD).send_keys(password)


def wait_visible(driver, locator):
    return WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located(locator))


def test_login_page_opens(driver, base_url):
    open_login_page(driver, base_url)

    assert driver.title == "Вход — TaskFlow"
    assert driver.find_element(*SUBMIT).text == "Войти"
    assert driver.find_element(*PASSWORD).get_attribute("type") == "password"


def test_successful_login(driver, base_url):
    """Задание 3: валидные данные → успешный вход, появляется кнопка «Выйти» (Logout)."""
    open_login_page(driver, base_url)
    fill_credentials(driver, VALID_LOGIN, VALID_PASSWORD)
    driver.find_element(*SUBMIT).click()

    logout = wait_visible(driver, LOGOUT)
    assert logout.text == "Выйти"
    assert driver.current_url.endswith("/app.html")
    assert driver.find_element(*CURRENT_USER).text == VALID_LOGIN

    ARTIFACTS.mkdir(exist_ok=True)
    driver.save_screenshot(str(ARTIFACTS / "successful_login.png"))


def test_login_by_enter_key(driver, base_url):
    open_login_page(driver, base_url)
    fill_credentials(driver, VALID_LOGIN, VALID_PASSWORD + Keys.ENTER)

    assert wait_visible(driver, LOGOUT).is_displayed()


@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        ("student", "wrong-pass", "Неверный логин или пароль"),
        ("nobody", VALID_PASSWORD, "Неверный логин или пароль"),
        ("Student", VALID_PASSWORD, "Неверный логин или пароль"),
        ("locked", VALID_PASSWORD, "Учётная запись заблокирована"),
        ("", "", "Введите логин и пароль"),
    ],
    ids=["wrong_password", "unknown_user", "login_case_sensitive", "locked_user", "empty_fields"],
)
def test_invalid_login(driver, base_url, username, password, message):
    open_login_page(driver, base_url)
    fill_credentials(driver, username, password)
    driver.find_element(*SUBMIT).click()

    assert wait_visible(driver, ERROR).text == message
    assert driver.current_url.endswith("/login.html")
    assert not driver.find_elements(*LOGOUT)


def test_logout(driver, base_url):
    open_login_page(driver, base_url)
    fill_credentials(driver, VALID_LOGIN, VALID_PASSWORD)
    driver.find_element(*SUBMIT).click()
    wait_visible(driver, LOGOUT).click()

    assert wait_visible(driver, LOGOUT_NOTICE).text == "Вы вышли из системы"
    assert "/login.html" in driver.current_url
