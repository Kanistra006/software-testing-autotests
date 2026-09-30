"""Позитивные сценарии формы обратной связи."""
import re

import pytest

from pages.contact_page import VALID_CONTACT, valid_contact


def test_submit_all_fields_valid(contact_page):
    """Задание 2: все поля заполнены валидными данными → сообщение об успешной отправке."""
    contact_page.send(VALID_CONTACT)

    message = contact_page.wait_success_message()
    assert contact_page.success_title() == "Обращение отправлено"
    assert re.fullmatch(
        r"Спасибо, Анна! Ваше обращение № \d{4} принято\. Ответ придёт на anna@example\.com\.", message
    )
    assert not contact_page.is_form_shown()
    assert contact_page.errors() == {}


def test_submit_required_fields_only(contact_page):
    """Телефон необязателен: форма отправляется без него."""
    contact_page.send(valid_contact(phone=""))

    assert contact_page.wait_success_message().startswith("Спасибо, Анна!")


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": "Ян"},                        # минимальная длина имени — 2
        {"name": "Я" * 50},                    # максимальная длина имени — 50
        {"name": "Анна-Мария"},
        {"name": "Mary Jane"},
        {"name": "  Анна  "},                  # пробелы по краям обрезаются
        {"email": "a.b-c@mail.co.uk"},
        {"phone": "89001234567"},
        {"phone": "8 (900) 123-45-67"},
        {"subject": "bug"},
        {"subject": "idea"},
        {"message": "Ровно 10 !"},             # минимальная длина сообщения — 10
        {"message": "ж" * 1000},               # максимальная длина сообщения — 1000
    ],
    ids=["name_min_2", "name_max_50", "name_hyphen", "name_latin_space", "name_trim",
         "email_subdomain", "phone_8", "phone_brackets", "subject_bug", "subject_idea",
         "message_min_10", "message_max_1000"],
)
def test_valid_boundary_values(contact_page, overrides):
    contact_page.send(valid_contact(**overrides))

    assert contact_page.wait_success_message().startswith("Спасибо,")


def test_send_another_resets_form(contact_page):
    contact_page.send(VALID_CONTACT).wait_success_message()
    contact_page.send_another()

    assert contact_page.is_form_shown()
    assert contact_page.field_value("name") == ""
    assert contact_page.field_value("message") == ""
    assert contact_page.message_counter() == "0/1000"
