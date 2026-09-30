"""Бизнес-логика калькулятора SimpleCalc: арифметика, степень, проверка простоты числа."""

Number = int | float


def _check_numbers(*values) -> None:
    """Аргументы должны быть числами int или float. bool числом не считается."""
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Ожидалось число, получено {type(value).__name__}")


class Calculator:
    def add(self, a: Number, b: Number) -> Number:
        _check_numbers(a, b)
        return a + b

    def subtract(self, a: Number, b: Number) -> Number:
        _check_numbers(a, b)
        return a - b

    def multiply(self, a: Number, b: Number) -> Number:
        _check_numbers(a, b)
        return a * b

    def divide(self, a: Number, b: Number) -> float:
        _check_numbers(a, b)
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def power(self, base: Number, exponent: Number) -> Number:
        _check_numbers(base, exponent)
        if base == 0 and exponent < 0:
            raise ZeroDivisionError("Ноль нельзя возвести в отрицательную степень")
        if base < 0 and not float(exponent).is_integer():
            raise ValueError("Отрицательное число нельзя возвести в дробную степень")
        return base ** exponent

    def is_prime_number(self, n: int) -> bool:
        """Простое число — натуральное число больше 1, делящееся только на 1 и на себя."""
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Проверка простоты определена только для целых чисел")
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        divisor = 3
        while divisor * divisor <= n:
            if n % divisor == 0:
                return False
            divisor += 2
        return True
