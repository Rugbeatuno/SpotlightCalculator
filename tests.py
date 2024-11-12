from calc import evaluate_expression, rounded_with_ellipsis
import math

# Basic arithmetic tests
assert math.isclose(evaluate_expression("1 + 2"), 3)
assert math.isclose(evaluate_expression("10 - 3"), 7)
assert math.isclose(evaluate_expression("4 * 5"), 20)
assert math.isclose(evaluate_expression("12 / 4"), 3.0)
assert math.isclose(evaluate_expression("7 + 3 - 5"), 5)
assert math.isclose(evaluate_expression("3 * 2 + 5"), 11)
assert math.isclose(evaluate_expression("5 - 4 + 7"), 8)
assert math.isclose(evaluate_expression("8 / 2 * 3"), 12.0)
assert math.isclose(evaluate_expression("8 / 2 / 2"), 2.0)

# Order of operations tests
assert math.isclose(evaluate_expression("2 + 3 * 4"), 14)
assert math.isclose(evaluate_expression("(2 + 3) * 4"), 20)
assert math.isclose(evaluate_expression("10 / 2 + 5"), 10.0)
assert math.isclose(evaluate_expression("10 / (2 + 3)"), 2.0)
assert math.isclose(evaluate_expression("4 + 5 * 6 - 3"), 31)
assert math.isclose(evaluate_expression("(4 + 5) * (6 - 3)"), 27)
assert math.isclose(evaluate_expression("5 + 2 * (3^2) - 7"), 16)
assert math.isclose(evaluate_expression("10 - 5 * 2 + 3"), 3)
assert math.isclose(evaluate_expression("2^3 * 4 / 8"), 4.0)
assert math.isclose(evaluate_expression("(2^3) * (4 / 8)"), 4.0)

assert math.isclose(evaluate_expression("3 + 5 * 2"),
                    13)  # Multiplication before addition
# Mixed addition, multiplication, and subtraction
assert math.isclose(evaluate_expression("3 + 5 * 2 - 4"), 9)
assert math.isclose(evaluate_expression("10 / 2 + 5"),
                    10.0)  # Division before addition
assert math.isclose(evaluate_expression("10 - 4 / 2"),
                    8.0)  # Division before subtraction
# Multiplication and division before addition
assert math.isclose(evaluate_expression("2 * 3 + 4 / 2"), 8.0)
# Parentheses and exponentiation
assert math.isclose(evaluate_expression("3 + 4 * 2 / (1 - 5)^2"), 3.5)
assert math.isclose(evaluate_expression("(2 + 3) * 4"),
                    20)  # Parentheses override order
assert math.isclose(evaluate_expression("5 + 2 * (3^2) - 7"),
                    16)  # Exponentiation within parentheses
# Exponentiation after addition in parentheses
assert math.isclose(evaluate_expression("2^(3 + 2)"), 32)
# Exponentiation with parentheses before power
assert math.isclose(evaluate_expression("(3 + 2)^3"), 125)

# Exponentiation before multiplication
assert math.isclose(evaluate_expression("2^3 * 4"), 32)
# Multiplication after exponentiation
assert math.isclose(evaluate_expression("4 * 2^3"), 32)
# Multiplication after exponentiation
assert math.isclose(evaluate_expression("2 * 3^2"), 18)
# Exponentiation inside parentheses
assert math.isclose(evaluate_expression("3 + 4 * 2 / (1 - 5)^2"), 3.5)
assert math.isclose(evaluate_expression("2^(3 + 2)"), 32)  # Exponentiation

# Exponentiation tests
assert math.isclose(evaluate_expression("2^3"), 8)
assert math.isclose(evaluate_expression("4^0.5"), 2.0)
assert math.isclose(evaluate_expression("9^(1/2)"), 3.0)
assert math.isclose(evaluate_expression("10^(2 + 1)"), 1000)
assert math.isclose(evaluate_expression("2^(3 + 2)"), 32)
assert math.isclose(evaluate_expression("5^3"), 125)
assert math.isclose(evaluate_expression("16^(1/4)"), 2.0)
assert math.isclose(evaluate_expression("3^4"), 81)
assert math.isclose(evaluate_expression("2^(3 * 2)"), 64)

# Basic trigonometric functions (radians)
assert math.isclose(evaluate_expression("sin(pi/2)"), 1.0)
assert math.isclose(evaluate_expression("cos(0)"), 1.0)
assert math.isclose(evaluate_expression("tan(pi/4)"), 1.0)
assert math.isclose(evaluate_expression("sin(pi)"), 0.0)
assert math.isclose(evaluate_expression("cos(pi)"), -1.0)
assert math.isclose(evaluate_expression("tan(0)"), 0.0)
assert math.isclose(evaluate_expression("sin(pi/6)"), 0.5)
assert math.isclose(evaluate_expression("cos(pi/3)"), 0.5)
assert math.isclose(evaluate_expression("tan(pi/3)"), math.sqrt(3))

# Trigonometric functions with degrees notation
assert math.isclose(evaluate_expression("sin30deg"), 0.5)
assert math.isclose(evaluate_expression("cos45deg"), math.sqrt(2) / 2)
assert math.isclose(evaluate_expression("tan60deg"), math.sqrt(3))
assert math.isclose(evaluate_expression("cos90deg"), 0.0)
assert math.isclose(evaluate_expression("sin0deg"), 0.0)
assert math.isclose(evaluate_expression("tan45deg"), 1.0)
assert math.isclose(evaluate_expression("sin180deg"), 0.0)
assert math.isclose(evaluate_expression("cos270deg"), 0.0)
assert math.isclose(evaluate_expression("tan30deg"), math.sqrt(3) / 3)

# Inverse trigonometric functions
assert math.isclose(evaluate_expression("arcsin(0.5)"), math.pi / 6)
assert math.isclose(evaluate_expression("arccos(0.5)"), math.pi / 3)
assert math.isclose(evaluate_expression("arctan(1)"), math.pi / 4)
assert math.isclose(evaluate_expression("arcsin(1)"), math.pi / 2)
assert math.isclose(evaluate_expression("arccos(-1)"), math.pi)
assert math.isclose(evaluate_expression("arctan(0)"), 0.0)
assert math.isclose(evaluate_expression("arcsin(-0.5)"), -math.pi / 6)
assert math.isclose(evaluate_expression("arccos(0)"), math.pi / 2)
assert math.isclose(evaluate_expression("arctan(-1)"), -math.pi / 4)

# Sec, Cot, Csc tests
assert math.isclose(evaluate_expression("sec(pi/3)"), 2.0)
assert math.isclose(evaluate_expression("cot(pi/4)"), 1.0)
assert math.isclose(evaluate_expression("csc(pi/6)"), 2.0)
assert math.isclose(evaluate_expression("sec(0)"), 1.0)
assert math.isclose(evaluate_expression("cot(pi/2)"), 0.0)
assert math.isclose(evaluate_expression("csc(pi/2)"), 1.0)
assert math.isclose(evaluate_expression("sec(pi)"), -1.0)
assert evaluate_expression("cot(pi)") == 'Undefined'
assert math.isclose(evaluate_expression("csc(2*pi/3)"), 2 / math.sqrt(3))

# Square roots and logarithmic functions
assert math.isclose(evaluate_expression("sqrt(16)"), 4.0)
assert math.isclose(evaluate_expression("sqrt(2)"), math.sqrt(2))
assert math.isclose(evaluate_expression("sqrt(9)"), 3.0)
assert math.isclose(evaluate_expression("sqrt(25)"), 5.0)
assert math.isclose(evaluate_expression("ln(e)"), 1.0)
assert math.isclose(evaluate_expression("log(100)"), 2.0)
assert math.isclose(evaluate_expression("log(10^2)"), 2.0)
assert math.isclose(evaluate_expression("ln(e^3)"), 3.0)
assert math.isclose(evaluate_expression("log(1000)"), 3.0)

# Order of operations tests including factorial
assert math.isclose(evaluate_expression("3 + 5 * 2"),
                    13)  # Multiplication before addition
# Mixed addition, multiplication, and subtraction
assert math.isclose(evaluate_expression("3 + 5 * 2 - 4"), 9)
assert math.isclose(evaluate_expression("10 / 2 + 5"),
                    10.0)  # Division before addition
assert math.isclose(evaluate_expression("10 - 4 / 2"),
                    8.0)  # Division before subtraction
# Multiplication and division before addition
assert math.isclose(evaluate_expression("2 * 3 + 4 / 2"), 8.0)
# Parentheses and exponentiation
assert math.isclose(evaluate_expression("3 + 4 * 2 / (1 - 5)^2"), 3.5)
assert math.isclose(evaluate_expression("(2 + 3) * 4"),
                    20)  # Parentheses override order
assert math.isclose(evaluate_expression("5 + 2 * (3^2) - 7"),
                    16)  # Exponentiation within parentheses
# Exponentiation after addition in parentheses
assert math.isclose(evaluate_expression("2^(3 + 2)"), 32)
# Exponentiation with parentheses before power
assert math.isclose(evaluate_expression("(3 + 2)^3"), 125)

# Factorial order of operations tests
# Factorial before addition (3! = 6 + 4 = 10)
assert math.isclose(evaluate_expression("3! + 4"), 10)
# Factorial before multiplication (3! = 6, then 2 * 6 = 12)
assert math.isclose(evaluate_expression("2 * 3!"), 12)
# Factorial before exponentiation (3! = 6, then 6^2 = 36)
assert math.isclose(evaluate_expression("3!^2"), 36)
# Parentheses with factorial (3! = 6, then 4 + 6 = 10)
assert math.isclose(evaluate_expression("4 + (3!)"), 10)
# Factorial after parentheses (3 + 2 = 5, then 5! = 120)
assert math.isclose(evaluate_expression("(3 + 2)!"), 120)
# Factorial before multiplication and addition (3! = 6, 6 * 2 + 2 = 14)
assert math.isclose(evaluate_expression("2 + 3! * 2"), 14)
# Factorial with division (4! = 24, 2! = 2, then 24 / 2 = 12)
assert math.isclose(evaluate_expression("4! / 2!"), 12)
# Factorial with parentheses and division (5! = 120, 3! = 6, 2! = 2, then 120 / (6 * 2) = 10)
assert math.isclose(evaluate_expression("5! / (3! * 2!)"), 10)

# Complex and lengthy expressions
assert math.isclose(evaluate_expression("3 + 4 * 2 / (1 - 5)^2"), 3.5)
assert math.isclose(evaluate_expression(
    "(1/2 * 30^2) / (9.8 * sin30deg + 9.8 * cos30deg * 0.3)"), 60.43420211859144)
assert math.isclose(evaluate_expression(
    "2^(3 + 2) + sqrt(49) - log(1000)"), 36.0)  # log(1000) is base-10
assert math.isclose(evaluate_expression(
    # ln(e^2) is natural log
    "cos45deg + sin30deg + tan60deg + ln(e^2)"), 4.9391575888)
assert math.isclose(evaluate_expression(
    # log(100) is base-10
    "5 * cos45deg - log(100) + 3 * sqrt(16) + 2^3"), 21.5355339059)
assert math.isclose(evaluate_expression(
    "(5 + 3 * (2 + 8) / 4 - 3^2) * 2 + sec(pi/3) + csc(pi/6)"), 11)
assert math.isclose(evaluate_expression(
    # log(100) is base-10
    "2 * sqrt(25) + 5 * log(100) + sin(pi/4) + tan(pi/6)"), 21.2844570504)
assert math.isclose(evaluate_expression(
    "arcsin(0.5) + arccos(0.5) + arctan(1) + sec(pi/4) + cot(pi/3) + csc(pi/3)"), 5.5024588601)
assert math.isclose(evaluate_expression(
    # log(1000) is base-10
    "2^(3^2) + log(1000) + sin(30deg) + tan(45deg) + sqrt(64)"), 524.5)
assert math.isclose(evaluate_expression(
    '(1/2*30^2)/(9.8*sin30deg+9.8*cos30deg*.3)'), 60.43420211859144)

print('Passed Full Test Suite.')
