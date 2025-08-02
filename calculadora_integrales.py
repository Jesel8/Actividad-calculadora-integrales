# Calculadora de Integrales Definidas con Tkinter y Matplotlib
import tkinter as tk
from tkinter import Label, Button, Frame, Entry, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from sympy import symbols, sympify, lambdify, integrate, latex, pi, exp, sin, cos, tan, log, sqrt, oo

x = symbols('x')

math_dict = {
    'pi': pi,
    'π': pi,
    'e': exp(1),
    'E': exp(1),
    'exp': exp,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'ln': log,
    'log': log,
    'sqrt': sqrt,
    'oo': oo,
    '∞': oo,
    'x': x
}

class Style:
    PRIMARY = "#e63946"
    BG = "#f8f9fa"
    TEXT = "#1d3557"
    FONT = "Segoe UI"

    ENTRY = {
        "font": (FONT, 12),
        "bg": "#e9ecef",
        "fg": TEXT,
        "relief": "flat",
        "highlightthickness": 1,
        "highlightbackground": "#ced4da",
        "highlightcolor": PRIMARY
    }

    BUTTON = {
        "font": (FONT, 12),
        "bg": PRIMARY,
        "fg": BG,
        "activebackground": "#ff4d6e",
        "activeforeground": BG,
        "relief": "flat",
        "padx": 10,
        "pady": 5
    }

def plot_function(ax, func, a, b):
    ax.clear()
    f = lambdify(x, func, modules=["numpy"])

    x_vals = np.linspace(float(a)-2, float(b)+2, 1000)
    y_vals = f(x_vals)

    ax.plot(x_vals, y_vals, label="f(x)", color=Style.TEXT)
    ax.fill_between(x_vals, y_vals, where=(x_vals >= float(a)) & (x_vals <= float(b)), 
                    color=Style.PRIMARY, alpha=0.3, label="Área bajo la curva")

    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    ax.set_title("Gráfica de f(x)")

def calculate_integral():
    try:
        func_str = func_entry.get().strip().replace("^", "**")
        a = sympify(lower_limit_entry.get().strip(), locals=math_dict)
        b = sympify(upper_limit_entry.get().strip(), locals=math_dict)

        func = sympify(func_str, locals=math_dict)
        result_def = integrate(func, (x, a, b)).evalf()
        result_indef = integrate(func, x)

        result_label.config(
            text=f"∫ de {a} a {b} de f(x) dx = {result_def}\nIntegral indefinida: ∫f(x)dx = {latex(result_indef)} + C"
        )

        plot_function(ax, func, a, b)
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo calcular la integral: {e}")

def clear_input():
    func_entry.delete(0, tk.END)
    lower_limit_entry.delete(0, tk.END)
    upper_limit_entry.delete(0, tk.END)
    result_label.config(text="")
    ax.clear()
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Gráfica de f(x)")
    canvas.draw()

def insert_text(value):
    func_entry.insert(tk.INSERT, value)
    func_entry.focus()

def create_calculator_buttons(parent):
    buttons = [
        ['7', '8', '9', '+', '-'],
        ['4', '5', '6', '*', '/'],
        ['1', '2', '3', '(', ')'],
        ['0', '.', 'x', '^', 'sqrt('],
        ['sin(', 'cos(', 'tan(', 'ln(', 'log('],
        ['pi', 'e', 'oo', 'exp(', 'C']
    ]

    for i, row in enumerate(buttons):
        for j, val in enumerate(row):
            btn = Button(parent, text=val, width=5, command=lambda v=val: insert_text(v), **Style.BUTTON)
            btn.grid(row=i, column=j, padx=2, pady=2)

def create_gui():
    global func_entry, lower_limit_entry, upper_limit_entry, result_label, ax, canvas

    root = tk.Tk()
    root.title("Calculadora de Integrales Definidas")
    root.configure(bg=Style.BG)
    root.geometry("1000x700")

    input_frame = Frame(root, bg=Style.BG)
    input_frame.pack(pady=10)

    Label(input_frame, text="f(x):", bg=Style.BG, fg=Style.TEXT, font=(Style.FONT, 12)).grid(row=0, column=0, sticky="w")
    func_entry = Entry(input_frame, width=40, **Style.ENTRY)
    func_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(input_frame, text="Límite inferior (a):", bg=Style.BG, fg=Style.TEXT, font=(Style.FONT, 12)).grid(row=1, column=0, sticky="w")
    lower_limit_entry = Entry(input_frame, width=15, **Style.ENTRY)
    lower_limit_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    Label(input_frame, text="Límite superior (b):", bg=Style.BG, fg=Style.TEXT, font=(Style.FONT, 12)).grid(row=2, column=0, sticky="w")
    upper_limit_entry = Entry(input_frame, width=15, **Style.ENTRY)
    upper_limit_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    Button(input_frame, text="Calcular Integral", command=calculate_integral, **Style.BUTTON).grid(row=3, column=0, pady=10)
    Button(input_frame, text="Limpiar Entrada", command=clear_input, **Style.BUTTON).grid(row=3, column=1, pady=10)

    result_label = Label(root, text="", bg=Style.BG, fg=Style.TEXT, font=(Style.FONT, 14), justify="left")
    result_label.pack(pady=10)

    calc_frame = Frame(root, bg=Style.BG)
    calc_frame.pack(pady=5)
    create_calculator_buttons(calc_frame)

    fig = Figure(figsize=(7, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Gráfica de f(x)")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    canvas.draw()

    root.mainloop()

if __name__ == "__main__":
    create_gui()