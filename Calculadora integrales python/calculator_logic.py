# Contiene la lógica matemática para evaluar e integrar funciones.
from sympy import symbols, sympify, integrate, latex, pi, exp, sin, cos, tan, log, sqrt, oo
import numpy as np

# Definimos el símbolo 'x' que usaremos en todas las funciones
x = symbols('x')

# Diccionario de funciones y constantes matemáticas permitidas
MATH_CONSTANTS = {
    'pi': pi,
    'π': pi,
    'e': exp(1),
    'E': exp(1),
    'oo': oo,
    '∞': oo,
}
MATH_FUNCTIONS = {
    'exp': exp,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'ln': log,
    'log': log,
    'sqrt': sqrt,
}
# Unimos todos los símbolos permitidos en un solo diccionario local
ALLOWED_SYMBOLS = {**MATH_CONSTANTS, **MATH_FUNCTIONS, 'x': x}

def parse_expression(expr_str):
    """Convierte una cadena de texto en una expresión de SymPy."""
    return sympify(expr_str.strip().replace("^", "**"), locals=ALLOWED_SYMBOLS)

def calculate_definite_integral(func, lower_limit, upper_limit):
    """Calcula la integral definida de una función."""
    a = parse_expression(lower_limit)
    b = parse_expression(upper_limit)
    result = integrate(func, (x, a, b))
    return result.evalf()

def calculate_indefinite_integral(func):
    """Calcula la integral indefinida de una función."""
    result = integrate(func, x)
    return result

def generate_plot_data(func, lower_limit, upper_limit):
    """Genera los puntos necesarios para graficar la función."""
    f = lambdify(x, func, modules=["numpy"])
    a_float = float(parse_expression(lower_limit).evalf())
    b_float = float(parse_expression(upper_limit).evalf())
    
    # Rango extendido para una mejor visualización
    x_vals = np.linspace(a_float - 2, b_float + 2, 1000)
    y_vals = f(x_vals)
    
    return x_vals, y_vals, a_float, b_float