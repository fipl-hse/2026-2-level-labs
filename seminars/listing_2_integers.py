"""
Programming 2026.

Seminar 2.
Integers and float data.
"""

# pylint: disable=invalid-name, unused-argument, redefined-outer-name

# Common information about numbers
#
# integers (int) are whole numbers (positive, negative, or zero)
# floating-point numbers (float) represent decimal values
# numbers are immutable
# numbers are not iterable
# arithmetic operations can be applied: +, -, *, /, //, %, **

# Create numbers
# a = 10  # int
# b = 3.5  # float
# print(a, b)

# # Basic arithmetic operations
# print(a + b)  # addition
# print(a - b)  # subtraction
# print(a * b)  # multiplication
# print(a / b)  # division (always float)
# print(a // 3)  # integer division
# print(a % 3)  # modulus (remainder)
# print(a**2)  # exponentiation

# # Type conversion
# print(int(3.9))  # convert float to int → 3
# print(float(7))  # convert int to float → 7.0

# Useful functions for numbers (some of them)
# abs(x)       → absolute value of x
# round(x, n)  → round x to n decimal places
# pow(a, b)    → a raised to the power of b
# divmod(a, b) → returns a tuple (a // b, a % b)
# max(a, b, …) → the largest value
# min(a, b, …) → the smallest value
# sum(iterable) → sum of all elements in an iterable


# TASKS


# Task 1:
def add_numbers(a: int, b: int) -> int:
    """
    Return the sum of two integers.

    Args:
        a (int): First integer
        b (int): Second integer

    Returns:
        int: Sum of a and b
    """
    # student implementation goes here
    int_sum = a + b
    return int_sum


# print(add_numbers(2, 3))
# print(add_numbers(-5, 10))
# print(add_numbers(0, 0))


# Task 2:
def average(a: float, b: float, c: float) -> float:
    """
    Calculate the average of three numbers.

    Args:
        a (float): First number
        b (float): Second number
        c (float): Third number

    Returns:
        float: Average value of the three numbers
    """
    # student implementation goes here
    n_numbers = 3
    sum_numbers = a + b + c
    average_numbers = sum_numbers / n_numbers
    return average_numbers

# print(average(1, 2, 3))
# print(average(10, 20, 30))
# print(average(5.5, 6.5, 7.5))


# Task 3:
def is_even(n: int) -> bool:
    """
    Check if a number is even.

    Args:
        n (int): Number to check

    Returns:
        bool: True if n is even, False otherwise
    """
    # student implementation goes here
    return n % 2 == 0

# print(is_even(2))
# print(is_even(3))
# print(is_even(0))
# print(is_even(-4))


# Task 4:
def area_of_circle(radius: float) -> float:
    """
    Calculate the area of a circle.

    Args:
        radius (float): Radius of the circle

    Returns:
        float: Area of the circle
    """
    # student implementation goes here
    circle_area = 3.14159 * radius**2
    return circle_area

# print(area_of_circle(1))
# print(area_of_circle(0))
# print(area_of_circle(2.5))


# Task 5:
def factorial(n: int) -> int:
    """
    Calculate the factorial of a number.

    Args:
        n (int): Non-negative integer

    Returns:
        int: Factorial of n
    """
    # student implementation goes here
    fact = 1
    if n > 1:
        for num in range(2, n + 1):
            fact *= num
    return fact

# print(factorial(0))
# print(factorial(1))
# print(factorial(5))


# Task 6:
def power(a: float, b: int) -> float:
    """
    Raise a number to a power.

    Args:
        a (float): Base number
        b (int): Exponent

    Returns:
        float: Result of a raised to the power of b
    """
    # student implementation goes here
    powered_num = a ** b
    return powered_num

# print(power(2, 3))
# print(power(5, 0))
# print(power(2, -2))


# Task 7:
def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate the Euclidean distance between two points.
    Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Args:
        x1 (float): x-coordinate of the first point
        y1 (float): y-coordinate of the first point
        x2 (float): x-coordinate of the second point
        y2 (float): y-coordinate of the second point

    Returns:
        float: Euclidean distance between the two points
    """
    # student implementation goes here
    e_distance =((x2-x1)**2 + (y2 - y1)**2) ** 0.5
    return e_distance

# print(distance(0, 0, 3, 4))
# print(distance(1, 2, 1, 2))
# print(distance(-1, -1, 2, 3))


# Task 8 (advanced):
def fibonacci(n: int) -> int:
    """
    Return the n-th Fibonacci number (0-indexed).

    Args:
        n (int): Index in the Fibonacci sequence (0 or greater)

    Returns:
        int: n-th Fibonacci number
    """
    # student implementation goes here
    if n == 0:
        return 0

    f0 = 0
    f1 = 1
    i = 1
    while i < n:
        f2 = f0 + f1
        f0 = f1
        f1 = f2
        i += 1
    return f1

# print(fibonacci(0))
# print(fibonacci(1))
# print(fibonacci(5))
# print(fibonacci(7))


# Task 9 (advanced):
def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n (int): Integer greater than or equal to 2

    Returns:
        bool: True if n is prime, False otherwise
    """

