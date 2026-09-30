# Автотесты по курсу «Тестирование программного обеспечения»

[![Run tests](https://github.com/Kanistra006/software-testing-autotests/actions/workflows/run-tests.yml/badge.svg)](https://github.com/Kanistra006/software-testing-autotests/actions/workflows/run-tests.yml)

Автотесты из лабораторных работ, которые автоматически запускаются в GitHub Actions при каждом push
(`.github/workflows/run-tests.yml`).

| Папка | Что тестируется | Инструменты | Тестов |
|---|---|---|---|
| `lab6_unit_tests` | Класс `Calculator`: add, subtract, multiply, divide (включая деление на ноль), power, is_prime_number | pytest, параметризация, pytest-cov | 179 |
| `lab3_selenium_login` | Страница входа: успешный вход (кнопка «Выйти»), неверные данные, выход | Selenium WebDriver, webdriver-manager | 9 |
| `lab4_page_object` | Форма обратной связи: позитивные и негативные сценарии, матрица решений (96 комбинаций) | Selenium, Page Object (`BasePage`, `ContactPage`) | 131 |

UI-тесты сами поднимают локальный стенд (папка `stand/` в каждой лабораторной) и запускают Chrome.

## Workflow

Для каждого набора тестов — отдельное задание в матрице:

1. `ubuntu-latest` — виртуальная машина GitHub с Linux и Google Chrome;
2. `actions/setup-python` — Python 3.11 с кэшем pip;
3. `pip install -r requirements.txt` — зависимости;
4. `python -m pytest` — запуск тестов (`HEADLESS=1`, Chrome без окна);
5. `actions/upload-artifact` — отчёт JUnit XML и скриншоты упавших тестов.

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

cd lab6_unit_tests && python -m pytest
cd lab3_selenium_login && python -m pytest --headless
cd lab4_page_object && python -m pytest --headless
```
