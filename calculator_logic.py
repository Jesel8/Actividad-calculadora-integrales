# calculator_logic.py (Versión Corregida y Mejorada)

# Contiene la lógica matemática para evaluar e integrar funciones.
import re  # <--- PASO 1.1: AÑADIR ESTE IMPORT
from sympy import (
    symbols,
    sympify,
    integrate,
    latex,
    lambdify,
    pi,
    exp,
    sin,
    cos,
    tan,
    log,
    sqrt,
    oo,
)
import numpy as np

# Definimos el símbolo 'x' que usaremos en todas las funciones
x = symbols("x")

# Diccionario de funciones y constantes matemáticas permitidas
MATH_CONSTANTS = {
    "pi": pi,
    "π": pi,
    "e": exp(1),
    "E": exp(1),
    "oo": oo,
    "∞": oo,
}
MATH_FUNCTIONS = {
    "exp": exp,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "ln": log,
    "log": log,
    "sqrt": sqrt,
}
ALLOWED_SYMBOLS = {**MATH_CONSTANTS, **MATH_FUNCTIONS, "x": x}


# vvvv PASO 1.2: REEMPLAZA TU FUNCIÓN parse_expression POR ESTA vvvv
def parse_expression(expr_str):
    """
    Convierte una cadena de texto en una expresión de SymPy,
    manejando la multiplicación implícita antes de la evaluación.
    """
    # Reemplaza el circunflejo por el operador de potencia de Python
    processed_str = expr_str.strip().replace("^", "**")

    # Expresiones regulares para añadir '*' donde haya multiplicación implícita:
    # Caso 1: Un número seguido de una letra o paréntesis de apertura (ej. 2x -> 2*x, 3( -> 3*()
    processed_str = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", processed_str)

    # Caso 2: Un paréntesis de cierre seguido de una letra o paréntesis de apertura (ej. )( -> )*(, )x -> )*x)
    processed_str = re.sub(r"([)])([a-zA-Z(])", r"\1*\2", processed_str)

    # Evaluar la expresión procesada con el diccionario de símbolos seguros
    return sympify(processed_str, locals=ALLOWED_SYMBOLS)


# ^^^^ FIN DEL REEMPLAZO ^^^^


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
    """
    Genera los puntos necesarios para graficar la función de forma robusta.
    """
    # Usamos lambdify para convertir la expresión de SymPy en una función numérica
    # que NumPy pueda entender.
    f = lambdify(x, func, modules=["numpy"])

    a_float, b_float = 0, 0
    try:
        # Intentamos evaluar los límites como números flotantes
        a_float = float(parse_expression(lower_limit).evalf())
        b_float = float(parse_expression(upper_limit).evalf())
    except (TypeError, AttributeError):
        # Si los límites no son numéricos (ej. infinito 'oo'), no podemos graficarlos.
        # En este caso, simplemente graficamos la función en un rango por defecto.
        a_float, b_float = -5, 5  # Usamos un rango estándar para la vista
        print(
            "Advertencia: Límites no numéricos, usando rango de [-5, 5] para la gráfica."
        )

    # Aseguramos un rango de visualización adecuado, incluso si los límites son iguales.
    view_min = min(a_float, b_float) - 2.5
    view_max = max(a_float, b_float) + 2.5

    # Caso especial: si el rango es cero (a=b), lo ampliamos para que la gráfica sea visible.
    if view_min == view_max:
        view_min -= 5
        view_max += 5

    # Generamos 1000 puntos en el rango de visualización para una curva suave.
    x_vals = np.linspace(view_min, view_max, 1000)
    y_vals = f(x_vals)

    return x_vals, y_vals, a_float, b_float
