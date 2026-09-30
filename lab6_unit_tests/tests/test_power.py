"""Модульные тесты power."""
import pytest
from pytest import approx


@pytest.mark.parametrize(
    ("base", "exponent", "expected"),
    [
        (2, 10, 1024),
        (5, 0, 1),
        (0, 0, 1),                 # соглашение Python: 0 ** 0 == 1
        (0, 5, 0),
        (-2, 3, -8),
        (-2, 2, 4),
        (-2, 2.0, 4.0),            # дробный тип, но целое значение — допустимо
        (2, -2, 0.25),
        (9, 0.5, 3.0),
        (1.5, 2, 2.25),
        (10, 20, 10**20),
    ],
    ids=["positive", "zero_exponent", "zero_to_zero", "zero_base", "negative_odd", "negative_even",
         "negative_float_integer_exp", "negative_exponent", "square_root", "float_base", "big_int"],
)
def test_power(calc, base, exponent, expected):
    assert calc.power(base, exponent) == approx(expected)


@pytest.mark.parametrize("exponent", [-1, -2, -0.5])
def test_zero_to_negative_power_raises(calc, exponent):
    with pytest.raises(ZeroDivisionError, match="Ноль нельзя возвести в отрицательную степень"):
        calc.power(0, exponent)


@pytest.mark.parametrize(("base", "exponent"), [(-8, 1 / 3), (-4, 0.5), (-1, 2.5)])
def test_negative_base_fractional_exponent_raises(calc, base, exponent):
    # без проверки Python вернул бы комплексное число
    with pytest.raises(ValueError, match="Отрицательное число нельзя возвести в дробную степень"):
        calc.power(base, exponent)
