from calc import format_equation, conversions
import numpy as np

equation = 'arcsin(x)'
formatted = format_equation(equation)
conversions['x'] = np.array([i for i in range(300)])
res = eval(formatted, conversions)
print(formatted, res)
