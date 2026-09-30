"""Модульные тесты is_prime_number."""
import pytest

PRIMES = [2, 3, 5, 7, 11, 13, 17, 97, 101, 7919, 104729, 2_147_483_647]
NOT_PRIMES = [4, 6, 8, 9, 15, 21, 25, 49, 91, 561, 1001, 7917, 1_000_000, 2_147_483_649]
BELOW_TWO = [1, 0, -1, -2, -7, -97]


@pytest.mark.parametrize("n", PRIMES)
def test_prime_numbers(calc, n):
    assert calc.is_prime_number(n) is True


@pytest.mark.parametrize("n", NOT_PRIMES)
def test_composite_numbers(calc, n):
    # 9, 25, 49 — квадраты простых (граница цикла divisor² <= n); 91 = 7·13; 561 — число Кармайкла
    assert calc.is_prime_number(n) is False


@pytest.mark.parametrize("n", BELOW_TWO)
def test_numbers_below_two_are_not_prime(calc, n):
    assert calc.is_prime_number(n) is False


def test_primes_up_to_100(calc):
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    assert [n for n in range(101) if calc.is_prime_number(n)] == expected


@pytest.mark.parametrize("value", [7.0, 2.5, "7", None, True], ids=["float_int_value", "float", "str", "none", "bool"])
def test_is_prime_rejects_non_integers(calc, value):
    with pytest.raises(TypeError, match="только для целых чисел"):
        calc.is_prime_number(value)
