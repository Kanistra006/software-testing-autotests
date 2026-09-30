"""Негативные сценарии формы обратной связи."""
import pytest

from pages.contact_page import valid_contact


@pytest.mark.parametrize(
    ("field", "empty_value", "expected_error"),
    [
        ("name", "", "Введите имя"),
        ("email", "", "Введите email"),
        ("subject", "", "Выберите тему обращения"),
        ("message", "", "Введите сообщение"),
        ("consent", False, "Необходимо согласие на обработку персональных данных"),
    ],
    ids=["name", "email", "subject", "message", "consent"],
)
def test_empty_required_field(contact_page, field, empty_value, expected_error):
    """Задание 3: одно обязательное поле пустое → текст ошибки у этого поля, форма не отправлена."""
    contact_page.send(valid_contact(**{field: empty_value}))

    assert contact_page.wait_error(field) == expected_error
    assert contact_page.errors() == {field: expected_error}
    assert contact_page.is_marked_invalid(field)
    assert contact_page.active_element_id() == field  # фокус на ошибочном поле
    assert not contact_page.is_success_shown()


@pytest.mark.parametrize(
    ("field", "value", "expected_error"),
    [
        ("name", "А", "Имя: от 2 до 50 букв, допускаются пробел и дефис"),
        ("name", "Я" * 51, "Имя: от 2 до 50 букв, допускаются пробел и дефис"),
        ("name", "Анна1", "Имя: от 2 до 50 букв, допускаются пробел и дефис"),
        ("name", "   ", "Введите имя"),
        ("email", "anna.example.com", "Введите корректный email, например name@example.com"),
        ("email", "anna@", "Введите корректный email, например name@example.com"),
        ("email", "anna @example.com", "Введите корректный email, например name@example.com"),
        ("phone", "12345", "Телефон в формате +7 900 123-45-67"),
        ("phone", "+7 900 123-45-6", "Телефон в формате +7 900 123-45-67"),
        ("phone", "+7 900 123-45-678", "Телефон в формате +7 900 123-45-67"),
        ("message", "Девять ..", "Сообщение: от 10 до 1000 символов"),
        ("message", "          ", "Введите сообщение"),
    ],
    ids=["name_1_char", "name_51_chars", "name_digit", "name_spaces", "email_no_at", "email_no_domain",
         "email_space", "phone_short", "phone_10_digits", "phone_12_digits", "message_9_chars", "message_spaces"],
)
def test_invalid_field_value(contact_page, field, value, expected_error):
    contact_page.send(valid_contact(**{field: value}))

    assert contact_page.wait_error(field) == expected_error
    assert contact_page.errors() == {field: expected_error}
    assert not contact_page.is_success_shown()


def test_all_fields_empty(contact_page):
    contact_page.submit()

    contact_page.wait_error("name")
    assert contact_page.errors() == {
        "name": "Введите имя",
        "email": "Введите email",
        "subject": "Выберите тему обращения",
        "message": "Введите сообщение",
        "consent": "Необходимо согласие на обработку персональных данных",
    }
    assert contact_page.active_element_id() == "name"


def test_error_disappears_after_fix(contact_page):
    contact_page.send(valid_contact(email=""))
    assert contact_page.wait_error("email") == "Введите email"

    contact_page.fill_email("anna@example.com")
    assert contact_page.error("email") == ""
    assert not contact_page.is_marked_invalid("email")

    contact_page.submit()
    assert contact_page.wait_success_message().startswith("Спасибо, Анна!")


def test_message_longer_than_limit_is_cut(contact_page):
    contact_page.fill_message("ж" * 1001)

    assert len(contact_page.field_value("message")) == 1000
    assert contact_page.message_counter() == "1000/1000"
