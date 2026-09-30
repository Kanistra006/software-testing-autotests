import pytest

from calculator import Calculator


@pytest.fixture
def calc() -> Calculator:
    """Новый экземпляр калькулятора для каждого теста."""
    return Calculator()
