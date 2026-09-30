"""Базовый класс Page Object: общие действия и ожидания для всех страниц."""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

Locator = tuple[str, str]


class BasePage:
    PATH = ""  # адрес страницы относительно base_url, задаётся в наследнике

    def __init__(self, driver: WebDriver, base_url: str, timeout: float = 5):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    # --- навигация ---
    def open(self):
        self.driver.get(f"{self.base_url}/{self.PATH}")
        self.wait_until_loaded()
        return self

    def wait_until_loaded(self):
        """Наследник переопределяет: чего ждать, чтобы страница считалась загруженной."""

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    # --- поиск элементов ---
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_visible(self, locator: Locator) -> bool:
        """Проверка без ожидания: элемент есть на странице и отображается."""
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    # --- действия ---
    def click(self, locator: Locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: Locator, text: str, clear: bool = True):
        element = self.find_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def select_by_value(self, locator: Locator, value: str):
        Select(self.find_visible(locator)).select_by_value(value)

    def set_checkbox(self, locator: Locator, checked: bool):
        element = self.find_visible(locator)
        if element.is_selected() != checked:
            element.click()

    # --- чтение состояния ---
    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def attribute_of(self, locator: Locator, name: str) -> str | None:
        return self.find(locator).get_attribute(name)

    def wait_for_text(self, locator: Locator) -> str:
        """Дождаться, пока у элемента появится непустой текст, и вернуть его."""
        return self.wait.until(lambda d: d.find_element(*locator).text or False)

    def active_element_id(self) -> str | None:
        return self.driver.switch_to.active_element.get_attribute("id")
