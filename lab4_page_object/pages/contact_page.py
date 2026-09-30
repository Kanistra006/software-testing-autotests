"""Page Object формы обратной связи TaskFlow."""
from dataclasses import dataclass, replace

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


@dataclass(frozen=True)
class ContactData:
    """Данные для заполнения формы. subject — value пункта списка ("" — тема не выбрана)."""
    name: str
    email: str
    phone: str
    subject: str
    message: str
    consent: bool


VALID_CONTACT = ContactData(
    name="Анна",
    email="anna@example.com",
    phone="+7 900 123-45-67",
    subject="question",
    message="Не приходит уведомление о просроченной задаче.",
    consent=True,
)


def valid_contact(**overrides) -> ContactData:
    """Валидные данные; в overrides — поля, которые нужно заменить."""
    return replace(VALID_CONTACT, **overrides)


class ContactPage(BasePage):
    PATH = "contact.html"

    FORM = (By.ID, "contact-form")
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    SUBJECT = (By.ID, "subject")
    MESSAGE = (By.ID, "message")
    MESSAGE_COUNTER = (By.ID, "message-counter")
    CONSENT = (By.ID, "consent")
    SUBMIT = (By.ID, "submit")
    SUCCESS = (By.ID, "success")
    SUCCESS_TITLE = (By.ID, "success-title")
    SUCCESS_MESSAGE = (By.ID, "success-message")
    SEND_ANOTHER = (By.ID, "send-another")

    FIELDS = ("name", "email", "phone", "subject", "message", "consent")

    def wait_until_loaded(self):
        self.find_visible(self.FORM)

    @staticmethod
    def error_locator(field: str):
        return By.ID, f"{field}-error"

    # --- заполнение ---
    def fill_name(self, value: str):
        self.type(self.NAME, value)
        return self

    def fill_email(self, value: str):
        self.type(self.EMAIL, value)
        return self

    def fill_phone(self, value: str):
        self.type(self.PHONE, value)
        return self

    def choose_subject(self, value: str):
        self.select_by_value(self.SUBJECT, value)
        return self

    def fill_message(self, value: str):
        self.type(self.MESSAGE, value)
        return self

    def set_consent(self, checked: bool):
        self.set_checkbox(self.CONSENT, checked)
        return self

    def fill(self, data: ContactData):
        return (self.fill_name(data.name)
                .fill_email(data.email)
                .fill_phone(data.phone)
                .choose_subject(data.subject)
                .fill_message(data.message)
                .set_consent(data.consent))

    def submit(self):
        self.click(self.SUBMIT)
        return self

    def send(self, data: ContactData):
        """Заполнить форму и нажать «Отправить»."""
        return self.fill(data).submit()

    def send_another(self):
        self.click(self.SEND_ANOTHER)
        self.wait_until_loaded()
        return self

    # --- результат ---
    def wait_success_message(self) -> str:
        return self.find_visible(self.SUCCESS_MESSAGE).text

    def success_title(self) -> str:
        return self.text_of(self.SUCCESS_TITLE)

    def is_success_shown(self) -> bool:
        return self.is_visible(self.SUCCESS)

    def is_form_shown(self) -> bool:
        return self.is_visible(self.FORM)

    def wait_error(self, field: str) -> str:
        return self.wait_for_text(self.error_locator(field))

    def error(self, field: str) -> str:
        return self.text_of(self.error_locator(field))

    def errors(self) -> dict[str, str]:
        """Все непустые сообщения об ошибках: {поле: текст}."""
        return {f: text for f in self.FIELDS if (text := self.error(f))}

    def is_marked_invalid(self, field: str) -> bool:
        return self.attribute_of((By.ID, field), "aria-invalid") == "true"

    def field_value(self, field: str) -> str:
        return self.attribute_of((By.ID, field), "value")

    def message_counter(self) -> str:
        return self.text_of(self.MESSAGE_COUNTER)
