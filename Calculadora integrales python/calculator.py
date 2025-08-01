# Define la clase principal de la aplicación y su interfaz gráfica (GUI).
import tkinter as tk
from tkinter import Label, Button, Frame, Entry, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import latex

# Importamos nuestro propio código
from style import Style
import calculator_logic as calc

class IntegralCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Integrales Definidas")
        self.root.geometry("1000x700")
        self.root.configure(bg=Style.BACKGROUND)

        # Crear y organizar todos los widgets
        self._create_widgets()

    def _create_widgets(self):
        # Frame de entradas
        input_frame = Frame(self.root, bg=Style.BACKGROUND)
        input_frame.pack(pady=20)

        Label(input_frame, text="f(x):", bg=Style.BACKGROUND, fg=Style.TEXT_COLOR, font=(Style.FONT_FAMILY, 12)).grid(row=0, column=0, sticky="w", padx=5)
        self.func_entry = Entry(input_frame, width=40, **Style.ENTRY_STYLE)
        self.func_entry.grid(row=0, column=1, pady=5)

        Label(input_frame, text="Límite inferior (a):", bg=Style.BACKGROUND, fg=Style.TEXT_COLOR, font=(Style.FONT_FAMILY, 12)).grid(row=1, column=0, sticky="w", padx=5)
        self.lower_limit_entry = Entry(input_frame, width=15, **Style.ENTRY_STYLE)
        self.lower_limit_entry.grid(row=1, column=1, pady=5, sticky="w")

        Label(input_frame, text="Límite superior (b):", bg=Style.BACKGROUND, fg=Style.TEXT_COLOR, font=(Style.FONT_FAMILY, 12)).grid(row=2, column=0, sticky="w", padx=5)
        self.upper_limit_entry = Entry(input_frame, width=15, **Style.ENTRY_STYLE)
        self.upper_limit_entry.grid(row=2, column=1, pady=5, sticky="w")
        
        # Frame de botones de acción
        action_frame = Frame(input_frame, bg=Style.BACKGROUND)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)

        Button(action_frame, text="Calcular Integral", command=self.run_calculation, **Style.BUTTON_STYLE).pack(side="left", padx=10)
        Button(action_frame, text="Limpiar", command=self.clear_input, **Style.BUTTON_STYLE).pack(side="left", padx=10)

        # Label para mostrar resultados
        self.result_label = Label(self.root, text="", bg=Style.BACKGROUND, fg=Style.TEXT_COLOR, font=(Style.FONT_FAMILY, 14), justify="left")
        self.result_label.pack(pady=10)

        # Frame de la "calculadora" de botones
        calc_frame = Frame(self.root, bg=Style.BACKGROUND)
        calc_frame.pack(pady=5)
        self._create_calculator_buttons(calc_frame)
        
        # Área de la gráfica
        self._create_plot_area()

    def _create_plot_area(self):
        fig = Figure(figsize=(7, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor(Style.BACKGROUND)
        fig.patch.set_facecolor(Style.BACKGROUND)
        self.ax.tick_params(colors=Style.TEXT_COLOR)
        self.ax.spines['bottom'].set_color(Style.TEXT_COLOR)
        self.ax.spines['top'].set_color(Style.TEXT_COLOR) 
        self.ax.spines['right'].set_color(Style.TEXT_COLOR)
        self.ax.spines['left'].set_color(Style.TEXT_COLOR)

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.reset_plot()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def _create_calculator_buttons(self, parent):
        # Lógica para crear botones de la calculadora
        pass # La implementaremos después, es igual a la original pero usando los estilos nuevos
    
    def run_calculation(self):
        try:
            func_str = self.func_entry.get()
            a_str = self.lower_limit_entry.get()
            b_str = self.upper_limit_entry.get()

            if not all([func_str, a_str, b_str]):
                messagebox.showwarning("Entrada inválida", "Todos los campos son obligatorios.")
                return

            func = calc.parse_expression(func_str)
            
            res_def = calc.calculate_definite_integral(func, a_str, b_str)
            res_indef = calc.calculate_indefinite_integral(func)

            self.result_label.config(
                text=f"∫ de {a_str} a {b_str} de f(x) dx ≈ {res_def:.4f}\nIntegral indefinida: $ {latex(res_indef)} + C $"
            )

            self.plot_function(func, a_str, b_str)

        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"Hubo un error al procesar la función o los límites.\n\nDetalle: {e}")

    def plot_function(self, func, a, b):
        self.reset_plot(clear_all=False) # Solo limpia datos, no ejes
        x_vals, y_vals, a_float, b_float = calc.generate_plot_data(func, a, b)
        
        self.ax.plot(x_vals, y_vals, label=f"$ f(x) = {latex(func)} $", color=Style.TEXT_COLOR)
        self.ax.fill_between(x_vals, y_vals, where=((x_vals >= a_float) & (x_vals <= b_float)),
                              color=Style.PRIMARY, alpha=0.4, label="Área de la integral")
        self.ax.legend()
        self.canvas.draw()
    
    def clear_input(self):
        self.func_entry.delete(0, tk.END)
        self.lower_limit_entry.delete(0, tk.END)
        self.upper_limit_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.reset_plot()

    def reset_plot(self, clear_all=True):
        self.ax.clear()
        self.ax.grid(True, linestyle="--", alpha=0.3, color=Style.ACCENT)
        self.ax.axhline(0, color=Style.TEXT_COLOR, linewidth=0.8)
        self.ax.axvline(0, color=Style.TEXT_COLOR, linewidth=0.8)
        self.ax.set_title("Gráfica de la Función", color=Style.TEXT_COLOR)
        if hasattr(self, 'canvas'):
            self.canvas.draw()