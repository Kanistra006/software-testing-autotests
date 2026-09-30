"""Модульные тесты add, subtract, multiply."""
import pytest
from pytest import approx


class TestAdd:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (2, 3, 5),
            (-2, -3, -5),
            (-2, 3, 1),
            (0, 0, 0),
            (7, 0, 7),
            (10**20, 1, 10**20 + 1),       # целые Python не переполняются
            (2.5, 0.25, 2.75),
            (-1.5, 1.5, 0.0),
        ],
        ids=["positive", "negative", "mixed_signs", "zeros", "zero_is_neutral", "big_int",
             "floats", "opposite_floats"],
    )
    def test_add(self, calc, a, b, expected):
        assert calc.add(a, b) == expected

    def test_add_float_precision(self, calc):
        # 0.1 + 0.2 = 0.30000000000000004 в двоичной арифметике — сравниваем с допуском
        assert calc.add(0.1, 0.2) == approx(0.3)
        assert calc.add(0.1, 0.2) != 0.3

    @pytest.mark.parametrize(("a", "b"), [(3, 8), (-4.5, 2), (0, -7)])
    def test_add_is_commutative(self, calc, a, b):
        assert calc.add(a, b) == calc.add(b, a)


class TestSubtract:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (5, 3, 2),
            (3, 5, -2),
            (-5, -3, -2),
            (-5, 3, -8),
            (5, 0, 5),
            (0, 5, -5),
            (7, 7, 0),
            (5.5, 2.25, 3.25),
        ],
        ids=["positive_result", "negative_result", "both_negative", "mixed_signs",
             "minus_zero", "from_zero", "equal_numbers", "floats"],
    )
    def test_subtract(self, calc, a, b, expected):
        assert calc.subtract(a, b) == expected

    def test_subtract_is_inverse_of_add(self, calc):
        assert calc.subtract(calc.add(17, 25), 25) == 17


class TestMultiply:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (4, 5, 20),
            (-4, 5, -20),
            (-4, -5, 20),
            (123, 0, 0),
            (0, -9, 0),
            (7, 1, 7),
            (7, -1, -7),
            (2.5, 4, 10.0),
            (10**10, 10**10, 10**20),
        ],
        ids=["positive", "one_negative", "both_negative", "by_zero", "zero_by_negative",
             "by_one", "by_minus_one", "float_by_int", "big_int"],
    )
    def test_multiply(self, calc, a, b, expected):
        assert calc.multiply(a, b) == expected

    def test_multiply_float_precision(self, calc):
        assert calc.multiply(1.1, 3) == approx(3.3)
