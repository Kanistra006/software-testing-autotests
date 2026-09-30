"""Автоматический прогон всех 96 комбинаций матрицы принятия решений.

Для скорости используется один браузер на модуль: перед каждой комбинацией
страница открывается заново, поэтому комбинации не влияют друг на друга.
"""
import pytest

from decision_table import all_combinations
from pages.contact_page import ContactPage

COMBINATIONS = all_combinations()


@pytest.mark.parametrize("combo", COMBINATIONS, ids=[c.id for c in COMBINATIONS])
def test_decision_table(shared_driver, base_url, combo):
    page = ContactPage(shared_driver, base_url).open()
    page.send(combo.data)

    if combo.sent:
        assert page.wait_success_message().startswith("Спасибо, Анна!")
    else:
        page.wait_error(combo.invalid_fields[0])
        assert page.errors() == combo.expected_errors
        assert not page.is_success_shown()
