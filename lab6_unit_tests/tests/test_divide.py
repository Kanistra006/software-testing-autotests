"""Модульные тесты divide, включая деление на ноль."""
import pytest
from pytest import approx


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (10, 2, 5),
        (7, 2, 3.5),               # результат всегда float, не целочисленное деление
        (-10, 2, -5),
        (10, -4, -2.5),
        (-9, -3, 3),
        (0, 5, 0),
        (5, 1, 5),
        (2.5, 0.5, 5.0),
        (1, 10**6, 0.000001),
    ],
    ids=["exact", "fraction", "negative_dividend", "negative_divisor", "both_negative",
         "zero_dividend", "by_one", "floats", "small_result"],
)
def test_divide(calc, a, b, expected):
    assert calc.divide(a, b) == approx(expected)


def test_divide_returns_float(calc):
    result = calc.divide(10, 2)
    assert result == 5
    assert isinstance(result, float)


def test_divide_periodic_fraction(calc):
    assert calc.divide(1, 3) == approx(0.3333333333333333)
    assert calc.divide(2, 3) == approx(0.6666666666666666)


@pytest.mark.parametrize("dividend", [1, 0, -5, 2.5, 10**20], ids=["one", "zero", "negative", "float", "big_int"])
@pytest.mark.parametrize("zero", [0, 0.0, -0.0], ids=["int_zero", "float_zero", "negative_zero"])
def test_divide_by_zero_raises(calc, dividend, zero):
    """Задание 3: деление на ноль вызывает исключение ZeroDivisionError с понятным текстом."""
    with pytest.raises(ZeroDivisionError, match="^Деление на ноль невозможно$"):
        calc.divide(dividend, zero)


def test_divide_by_zero_exception_details(calc):
    with pytest.raises(ZeroDivisionError) as exc_info:
        calc.divide(42, 0)

    assert exc_info.type is ZeroDivisionError
    assert str(exc_info.value) == "Деление на ноль невозможно"


def test_divide_by_very_small_number_is_not_error(calc):
    assert calc.divide(1, 1e-300) == approx(1e300)


@pytest.mark.parametrize(("a", "b"), [(12, 4), (-7.5, 2.5), (1, 3), (10**9, 7)])
def test_divide_then_multiply_returns_dividend(calc, a, b):
    assert calc.multiply(calc.divide(a, b), b) == approx(a)
