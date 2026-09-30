"""Матрица принятия решений для формы обратной связи.

Каждое поле разбито на классы эквивалентности; из каждого класса взят один
представитель. Полный перебор классов даёт 2·2·3·2·2·2 = 96 комбинаций.
Правило формы: обращение отправляется, только если ни одно поле не невалидно.
"""
from dataclasses import dataclass
from itertools import product

from pages.contact_page import ContactData

# поле → {класс: (значение-представитель, валиден ли класс)}
CLASSES = {
    "name": {"В": ("Анна", True), "Н": ("Анна1", False)},
    "email": {"В": ("anna@example.com", True), "Н": ("anna@", False)},
    "phone": {"П": ("", True), "В": ("+7 900 123-45-67", True), "Н": ("12345", False)},
    "subject": {"В": ("question", True), "Н": ("", False)},
    "message": {"В": ("Не приходит уведомление о задаче.", True), "Н": ("Коротко", False)},
    "consent": {"В": (True, True), "Н": (False, False)},
}

# Тексты ошибок для невалидных представителей
ERRORS = {
    "name": "Имя: от 2 до 50 букв, допускаются пробел и дефис",
    "email": "Введите корректный email, например name@example.com",
    "phone": "Телефон в формате +7 900 123-45-67",
    "subject": "Выберите тему обращения",
    "message": "Сообщение: от 10 до 1000 символов",
    "consent": "Необходимо согласие на обработку персональных данных",
}

FIELD_TITLES = {"name": "Имя", "email": "Email", "phone": "Телефон",
                "subject": "Тема", "message": "Сообщение", "consent": "Согласие"}


@dataclass(frozen=True)
class Combination:
    id: str
    classes: dict  # поле → код класса
    data: ContactData
    invalid_fields: tuple

    @property
    def sent(self) -> bool:
        return not self.invalid_fields

    @property
    def expected_errors(self) -> dict:
        return {f: ERRORS[f] for f in self.invalid_fields}


def all_combinations() -> list[Combination]:
    fields = list(CLASSES)
    result = []
    for i, codes in enumerate(product(*(CLASSES[f] for f in fields)), 1):
        classes = dict(zip(fields, codes))
        values = {f: CLASSES[f][c][0] for f, c in classes.items()}
        invalid = tuple(f for f, c in classes.items() if not CLASSES[f][c][1])
        result.append(Combination(f"M{i:02d}", classes, ContactData(**values), invalid))
    return result
