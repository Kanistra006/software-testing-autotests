"""Проверка типов аргументов для всех арифметических методов."""
import pytest

METHODS = ["add", "subtract", "multiply", "divide", "power"]
INVALID = ["5", None, [1], {"a": 1}, True, 1 + 2j]
INVALID_IDS = ["str", "none", "list", "dict", "bool", "complex"]


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("bad", INVALID, ids=INVALID_IDS)
def test_invalid_first_argument(calc, method, bad):
    with pytest.raises(TypeError, match="Ожидалось число"):
        getattr(calc, method)(bad, 2)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("bad", INVALID, ids=INVALID_IDS)
def test_invalid_second_argument(calc, method, bad):
    with pytest.raises(TypeError, match="Ожидалось число"):
        getattr(calc, method)(2, bad)


def test_error_message_names_the_type(calc):
    with pytest.raises(TypeError) as exc_info:
        calc.add("5", 2)
    assert str(exc_info.value) == "Ожидалось число, получено str"
