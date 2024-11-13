import math

digits = '0123456789'
operations = '()+-/*'
trig_functions = ['sin', 'cos', 'tan', 'arcsin',
                  'arccos', 'arctan', 'sqrt', 'ln', 'log', 'sec', 'cot', 'csc', '√']


def cot(x):
    denom = rounded_with_ellipsis(math.tan(x))
    return "Undefined" if denom == 0 else 1 / denom


def sec(x):
    denom = rounded_with_ellipsis(math.cos(x))
    return "Undefined" if math.isclose(denom, 0) else 1 / denom


def csc(x):
    denom = rounded_with_ellipsis(math.sin(x))
    return "Undefined" if math.isclose(denom, 0) else 1 / denom


conversions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "csc": csc,
    "sec": sec,
    "cot": cot,
    "arcsin": math.asin,
    "arccos": math.acos,
    "arctan": math.atan,
    "log": math.log10,
    "ln": math.log,
    "log2": math.log2,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "e": math.e,
    '!': math.factorial

}


def get_all_indicies(string, expression):
    indices = []

    for i in range(len(expression)):
        if expression[i: i+len(string)].lower() == string:
            indices.append(i)
    return indices


def cvt_factorial(expression):
    # very challenging because factorial symbol comes after whatever needs to be factorialed, 5!
    # to tackle this, must find factorial symbols and look backwards and segment whichever part of the expression should be factorialed
    # could just look to the next sign prior, but that would break if there are parenthesis
    # so check if there are parenthesis first, then count parenthesis totals, otherwise could fail on something like this (3+5)! -> (3 + (5))!

    def single_pass(express):
        for i, char in enumerate(express):
            if char == '!':
                if express[i - 1] == ')':  # check parenthesis first
                    p_count = 0
                    for j in range(i-1, -1, -1):
                        if express[j] == ')':
                            p_count += 1
                        if express[j] == '(':
                            p_count -= 1

                        if p_count == 0:
                            inner_express = express[j:i]
                            value = evaluate_expression(inner_express)
                            factorialed = math.factorial(int(value))
                            express = express[:j] + \
                                f'({factorialed})' + express[i+1:]
                            return express
                else:
                    for j in range(i, -1, -1):
                        if express[j] in operations or j == 0:
                            inner_express = express[j +
                                                    1:i] if j != 0 else express[0:i]
                            factorialed = math.factorial(int(inner_express))
                            express = express[:j+1] + \
                                f'({factorialed})' + express[i+1:] if j != 0 else express[:j] + \
                                f'({factorialed})' + express[i+1:]
                            return express
        return express

    while '!' in expression:
        expression = single_pass(expression)
    return expression


def cvt_powers(expression):
    return expression.replace('^', '**')


def cvt_comparison(expression):
    return expression.replace('=', '==')


def cvt_constants(expression):
    expression = expression.replace('pi', f'({math.pi})')

    # e is more challenging because e is found in the word deg and sec
    if expression[0] == 'e':
        expression = f'({math.e})' + expression[1:]
    if expression[-1] == 'e':
        expression = expression[:-1] + f'({math.e})'

    for index in range(len(expression)-2, 0, -1):
        left = expression[index-1]
        char = expression[index]
        right = expression[index+1]

        if char == 'e' and left != 'd' and right != 'g' and left != 's' and right != 'c':
            expression = f'''{expression[:index]}({math.e}){
                expression[index+1:]}'''

    # expression = expression.replace('pi', math.pi)
    return expression


def catch_unclosed_parenthesis(expression):
    open_parenthesis_count = 0
    for char in expression:
        if char == '(':
            open_parenthesis_count += 1
        if char == ')':
            open_parenthesis_count -= 1

    return expression + ')' * open_parenthesis_count


def insert_parenthesis_around_trig(expression):
    last_operation_index = len(expression) - 1
    for i in range(len(expression)-1, -1, -1):
        if expression[i] in operations:
            last_operation_index = i

        for func in trig_functions:
            seek = expression[i-len(func):i]
            if seek == func and expression[last_operation_index] != '(':
                parenthesis = f'''({
                    expression[i-len(func) + len(func):last_operation_index]}'''

                if last_operation_index != len(expression) - 1:
                    parenthesis += ')'

                expression = expression[:i-len(func) + len(func)] + \
                    parenthesis + expression[last_operation_index:]
    return expression


def cvt_degrees(expression):
    # since the index of all 'deg' will be shifting use while loop

    def single_pass(start, express):
        value = ''
        for i in range(start-1, -1, -1):
            value = express[i] + value
            for func in trig_functions:
                if express[i-len(func)-1: i-1] == func:
                    express = express[:i] + \
                        str(math.radians(evaluate_expression(value))) + \
                        express[start:].replace('deg', '')

                    return express

    while True:
        deg_indices = get_all_indicies('deg', expression)
        if deg_indices:
            expression = single_pass(deg_indices[-1], expression)
        else:
            break
    return expression


def cvt_parenthesis_to_multi(expression):
    # 2(10), (10)2 doesnt evaluate so need to add mutliplication sign
    for d in digits:
        expression = expression.replace(f'{d}(', f'{d}*(')
        expression = expression.replace(f'){d}', f')*{d}')

    # 2sin(40deg), ()sin(40deg)
    for d in '0123456789)':
        for func in trig_functions:
            expression = expression.replace(f'{d}{func}', f'{d}*{func}')
            expression = expression.replace(f'{d}{func}', f'{d}*{func}')

    expression = expression.replace(')(', ')*(')
    return expression


def cvt_variables(expression, variables):
    for key in variables.keys():
        expression = expression.replace(key, f'({variables[key]})')
    return expression


def rounded_with_ellipsis(number, tolerance=1e-12):
    if isinstance(number, bool) or isinstance(number, str):
        return number

    # If the number is within the tolerance of a nearby integer, round to that integer
    if abs(number - round(number)) < tolerance:
        return round(number)

    for target in [0.5, math.sqrt(3), 0.125, 0.250, 0.750]:
        if abs(number - target) < tolerance:
            return target

    return number


def cvt_cleanup(expression):
    expression = expression.strip()
    expression = expression.replace(' ', '')
    expression = expression.replace(',', '')
    expression = expression.replace('"', '')
    expression = expression.replace("'", '')
    expression = expression.replace('√', 'sqrt')
    expression = expression.replace('π', 'pi')
    return expression


def evaluate_expression(expression, variables=None):

    # print(expression)
    result = ''

    expression = cvt_cleanup(expression)

    if variables:
        expression = cvt_variables(expression, variables)

    expression = cvt_factorial(expression)
    # print(1, expression)

    # add parenthesis around functions that need it
    expression = insert_parenthesis_around_trig(expression)
    # print(2, expression)

    # convert pi and e to numerical values
    expression = cvt_constants(expression)
    # print(3, expression)

    expression = cvt_parenthesis_to_multi(expression)
    # print(4, expression)

    # convert bitwise operation to power
    expression = cvt_powers(expression)

    # look for deg after a number to cvt degree to radians for internal calcualtion
    expression = cvt_degrees(expression)

    # catch unclosed parenthess
    expression = catch_unclosed_parenthesis(expression)

    # print(expression)
    result = eval(expression, {"__builtins__": None}, conversions)
    result = rounded_with_ellipsis(result)

    return result


if __name__ == '__main__':
    # cvt_factorial('5(3+(5))!')
    # cvt_factorial('3+5!')
    # nuke = '(1/2*30^2)/(9.8*sin30deg+9.8*cos30deg*.3)'
    print('Final Answer:', evaluate_expression(
        'x+3', {'x': 5}
    ))
    # print('Final Answer:', evaluate_expression(
    #     'tan(pi)'
    # ))
