"""
Programming 2026.

Seminar 18.
Data Type: Fraction.
"""

# pylint: disable=invalid-name, unused-argument


# =============================================================================
# Fraction: implementing a custom rational number type
# =============================================================================

# A fraction represents a rational number as numerator / denominator.
#
# Our goal is to implement a custom Fraction class and make it behave like
# a built-in Python type.
#
# During this seminar, we will explore different Python protocols:
#
# - Object protocol: __init__, __str__, __repr__
# - Numeric protocol: __add__, __sub__, __mul__, __truediv__
# - Comparison protocol: __eq__, __lt__, __le__, ...
# - Conversion protocol: __int__, __float__, __bool__
# - Arithmetic protocol: __floordiv__, __mod__, __pow__

# Important properties:
# - Fractions represent rational numbers exactly.
# - The denominator cannot be zero.
# - Fractions should always be stored in their reduced form.
# - The denominator should always be positive.
# - Fraction objects should be immutable (optional advanced task).


# Original source:
# github.com/python/cpython/blob/main/Lib/fractions.py


from typing import Any


class Fraction:
    """
    Custom implementation of a rational number.
    """

    def __init__(self, numerator: int, denominator: int = 1) -> None:
        """
        Initialize a reduced fraction with a positive denominator.

        Args:
            numerator (int): Numerator of the fraction.
            denominator (int): Denominator of the fraction. Defaults to 1.

        Raises:
            ZeroDivisionError: If the denominator is zero.

        Examples:
            Fraction(1, 2)
            Fraction(3)
        """

    def __str__(self) -> str:
        """
        Return a human-readable representation.

        Returns:
            str: The fraction in numerator/denominator form.
        """

    def __repr__(self) -> str:
        """
        Return an unambiguous representation.

        Returns:
            str: A constructor-style representation of the fraction.
        """

    def __add__(self, other: Any) -> Any:
        """
        Add another number to this fraction.

        Args:
            other (Any): Number to add.

        Returns:
            Fraction: The sum,
                or NotImplemented if the operand is unsupported.
        """

    def __sub__(self, other: Any) -> Any:
        """
        Subtract another number from this fraction.

        Args:
            other (Any): Number to subtract.

        Returns:
            Fraction: The difference,
                or NotImplemented if the operand is unsupported.
        """

    def __mul__(self, other: Any) -> Any:
        """
        Multiply this fraction by another number.

        Args:
            other (Any): Number to multiply by.

        Returns:
            Fraction: The product,
                or NotImplemented if the operand is unsupported.
        """

    def __truediv__(self, other: Any) -> Any:
        """
        Divide this fraction by another number.

        Args:
            other (Any): Divisor.

        Returns:
            Fraction: The quotient,
                or NotImplemented if the operand is unsupported.

        Raises:
            ZeroDivisionError: If the divisor is zero.
        """

    def __eq__(self, other: Any) -> Any:
        """
        Check whether this fraction equals another number.

        Args:
            other (Any): Number to compare against.

        Returns:
            bool: True if the values are equal, otherwise False,
                or NotImplemented if the operand is unsupported.
        """

    def __lt__(self, other: Any) -> Any:
        """
        Check whether this fraction is less than another number.

        Args:
            other (Any): Number to compare against.

        Returns:
            bool: True if this fraction is smaller, otherwise False,
                or NotImplemented if the operand is unsupported.
        """

    def __le__(self, other: Any) -> Any:
        """
        Check whether this fraction is less than or equal to another number.

        Args:
            other (Any): Number to compare against.

        Returns:
            bool: True if this fraction is smaller or equal, otherwise False.

        Raises:
            TypeError: If the operand does not support ordering with a fraction.
        """

    def __int__(self) -> int:
        """
        Convert the fraction to an integer.

        Returns:
            int: The quotient truncated toward zero.
        """

    def __float__(self) -> float:
        """
        Convert the fraction to a floating-point number.

        Returns:
            float: The numerator divided by the denominator.
        """

    def __bool__(self) -> bool:
        """
        Check whether the fraction is non-zero.

        Returns:
            bool: True if the numerator is non-zero, otherwise False.
        """

    def __floordiv__(self, other: Any) -> Any:
        """
        Divide this fraction and round the quotient down.

        Args:
            other (Fraction or int): Divisor.

        Returns:
            int: The quotient rounded down,
                or NotImplemented if the operand is unsupported.

        Raises:
            ZeroDivisionError: If the divisor is zero.
        """

    def __mod__(self, other: Any) -> Any:
        """
        Return the remainder after floor division.

        Args:
            other (Any): Divisor.

        Returns:
            Fraction: The remainder,
                or NotImplemented if the operand is unsupported.

        Raises:
            ZeroDivisionError: If the divisor is zero.
        """

    def __pow__(self, power: int) -> Any:
        """
        Raise the fraction to an integer power.

        Args:
            power (int): Exponent.

        Returns:
            Fraction: The resulting fraction, or NotImplemented if the exponent
                is unsupported.

        Raises:
            ZeroDivisionError: If zero is raised to a negative power.
        """


# =============================================================================
# Testing our implementation
# =============================================================================

# Uncomment the following examples as the corresponding methods are implemented.

# --- Construction and representation ---

# f1 = Fraction(2, 4)
# f2 = Fraction(1, 2)
# f3 = Fraction(3)
#
# print(f1)       # 1/2
# print(repr(f1)) # Fraction(1, 2)
# print(f3)       # 3/1


# --- Arithmetic operations ---

# a = Fraction(1, 2)
# b = Fraction(1, 3)
#
# print(a + b)  # 5/6
# print(a - b)  # 1/6
# print(a * b)  # 1/6
# print(a / b)  # 3/2
# print(a // b) # 1
# print(a % b)  # 1/6
# print(a ** 2) # 1/4


# --- Comparisons ---

# a = Fraction(1, 2)
# b = Fraction(2, 4)
# c = Fraction(3, 4)
#
# print(a == b)  # True
# print(a < c)   # True
# print(a <= b)  # True (requires __le__ or suitable implementation)


# --- Conversions ---

# f = Fraction(3, 2)
#
# print(int(f))    # 1
# print(float(f))  # 1.5
# print(bool(f))   # True
# print(bool(Fraction(0)))  # False
