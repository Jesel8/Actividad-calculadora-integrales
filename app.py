# app.py (VERSIÓN FINAL COMPLETA CON PDF Y SIN ERRORES DE ATRIBUTO)
import tkinter as tk
from tkinter import (
    Label,
    Button,
    Frame,
    Entry,
    messagebox,
    Menu,
    PhotoImage,
    filedialog,
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import latex
import os
import traceback
import pdf_generator  # Importamos nuestro nuevo módulo
from style import Style
import calculator_logic as calc
from history_window import HistoryWindow


# ===============================================================
# INICIO DE LA CLASE PRINCIPAL DE LA APLICACIÓN
# ===============================================================
class IntegralCalculatorApp:

    def __init__(self, root):
        self.root = root
        self.style = Style("dark")
        self.root.title("Calculadora de Integrales Definidas")
        self.root.geometry("1000x800")
        self.root.configure(bg=self.style.colors["BACKGROUND"])

        # Inicialización de todas las variables de estado
        self.frames_to_style, self.calc_buttons, self.icons, self.history = (
            [],
            [],
            {},
            [],
        )
        self.last_calculation_data = None

        # Llamadas a métodos de construcción
        self._load_icons()
        self._create_menu()
        self._create_widgets()
        self._create_status_bar()
        self.reset_plot()
        self.canvas.draw()

    # --- MÉTODOS DE CREACIÓN DE INTERFAZ ---
    def _load_icons(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "assets", "icons")
            self.icons["calculate"] = PhotoImage(
                file=os.path.join(icon_path, "calculate_icon.png")
            )
            self.icons["clear"] = PhotoImage(
                file=os.path.join(icon_path, "clear_icon.png")
            )
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar los iconos: {e}")
            self.icons.update({"calculate": None, "clear": None})

    def _create_menu(self):
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menú Archivo
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar a PDF...", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Menú Ver
        view_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Ver Historial", command=self._show_history_window)
        view_menu.add_separator()
        theme_menu = Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Tema", menu=theme_menu)
        theme_menu.add_command(
            label="Modo Oscuro", command=lambda: self._apply_theme("dark")
        )
        theme_menu.add_command(
            label="Modo Claro", command=lambda: self._apply_theme("light")
        )

        # Menú Ayuda
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self.show_about_info)

    def _create_widgets(self):
        # Todos los widgets se crean aquí
        main_frame = Frame(self.root, bg=self.style.colors["BACKGROUND"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.frames_to_style.append(main_frame)
        top_frame = Frame(main_frame, bg=self.style.colors["BACKGROUND"])
        top_frame.pack(side="top", fill="x", pady=(0, 20))
        self.frames_to_style.append(top_frame)
        input_frame = Frame(top_frame, bg=self.style.colors["BACKGROUND"])
        input_frame.grid(row=0, column=0, padx=(0, 20), sticky="ns")
        self.frames_to_style.append(input_frame)
        Label(input_frame, text="f(x):", **self.style.LABEL_STYLE).grid(
            row=0, column=0, sticky="e", padx=5, pady=8
        )
        self.func_entry = Entry(input_frame, width=35, **self.style.ENTRY_STYLE)
        self.func_entry.grid(row=0, column=1)
        Label(input_frame, text="Límite inferior (a):", **self.style.LABEL_STYLE).grid(
            row=1, column=0, sticky="e", padx=5, pady=8
        )
        self.lower_limit_entry = Entry(input_frame, width=20, **self.style.ENTRY_STYLE)
        self.lower_limit_entry.grid(row=1, column=1, sticky="w")
        Label(input_frame, text="Límite superior (b):", **self.style.LABEL_STYLE).grid(
            row=2, column=0, sticky="e", padx=5, pady=8
        )
        self.upper_limit_entry = Entry(input_frame, width=20, **self.style.ENTRY_STYLE)
        self.upper_limit_entry.grid(row=2, column=1, sticky="w")
        action_frame = Frame(input_frame, bg=self.style.colors["BACKGROUND"])
        action_frame.grid(row=3, column=0, columnspan=2, pady=15)
        self.frames_to_style.append(action_frame)
        self.calculate_button = Button(
            action_frame,
            text="Calcular",
            image=self.icons.get("calculate"),
            compound=tk.LEFT,
            command=self.run_calculation,
            **self.style.BUTTON_STYLE,
        )
        self.calculate_button.pack(side="left", padx=10)
        self.clear_button = Button(
            action_frame,
            text="Limpiar",
            image=self.icons.get("clear"),
            compound=tk.LEFT,
            command=self.clear_all,
            **self.style.BUTTON_STYLE,
        )
        self.clear_button.pack(side="left", padx=10)
        self._create_plot_area(top_frame)
        top_frame.grid_columnconfigure(1, weight=1)
        bottom_frame = Frame(main_frame, bg=self.style.colors["BACKGROUND"])
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        self.frames_to_style.append(bottom_frame)
        self.result_label = Label(
            bottom_frame,
            text="Ingrese una función para comenzar",
            **self.style.RESULT_LABEL_STYLE,
        )
        self.result_label.pack(pady=10)
        calc_frame = Frame(bottom_frame, bg=self.style.colors["BACKGROUND"])
        calc_frame.pack(pady=15)
        self.frames_to_style.append(calc_frame)
        self._create_calculator_buttons(calc_frame)

    def _create_plot_area(self, parent_frame):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    def _create_calculator_buttons(self, parent):
        buttons = [
            ["sin(", "cos(", "tan(", "^", "sqrt("],
            ["7", "8", "9", "/", "exp("],
            ["4", "5", "6", "*", "ln("],
            ["1", "2", "3", "-", "("],
            ["0", ".", "+", "e", ")"],
        ]
        [
            btn.grid(row=i, column=j, padx=3, pady=3) or self.calc_buttons.append(btn)
            for i, r in enumerate(buttons)
            for j, v in enumerate(r)
            for btn in [
                Button(
                    parent,
                    text=v,
                    width=5,
                    command=lambda v=v: self.insert_text(v),
                    **self.style.BUTTON_STYLE,
                )
            ]
        ]

    def _create_status_bar(self):
        self.status_bar = Label(
            self.root,
            text="Listo",
            relief=tk.SUNKEN,
            anchor="w",
            **self.style.LABEL_STYLE,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- LÓGICA PRINCIPAL ---
    def run_calculation(self, update_plot_only=False):
        try:
            if not update_plot_only:
                self.status_bar.config(text="Calculando...")
            func_str, a_str, b_str = (
                self.func_entry.get(),
                self.lower_limit_entry.get(),
                self.upper_limit_entry.get(),
            )
            if not all([func_str, a_str, b_str]):
                if not update_plot_only:
                    messagebox.showwarning(
                        "Entrada inválida", "Todos los campos son obligatorios."
                    )
                return
            func = calc.parse_expression(func_str)
            if not update_plot_only:
                res_def = calc.calculate_definite_integral(func, a_str, b_str)
                res_indef = calc.calculate_indefinite_integral(func)
                res_def_float = float(res_def)
                self.result_label.config(
                    text=f"∫ de {a_str} a {b_str} de f(x) dx ≈ {res_def_float:.4f}\nIntegral indefinida: $ {latex(res_indef)} + C $"
                )

                self.last_calculation_data = {
                    "func_str": func_str,
                    "a_str": a_str,
                    "b_str": b_str,
                    "result_def": f"{res_def_float:.4f}",
                    "result_indef_latex": f"$ {latex(res_indef)} + C $",
                }
                self.history.insert(0, self.last_calculation_data)
                if len(self.history) > 50:
                    self.history.pop()

            self.plot_function(func, a_str, b_str)
            if not update_plot_only:
                self.status_bar.config(text="Cálculo completado.")
        except Exception as e:
            if not update_plot_only:
                messagebox.showerror(
                    "Error de Cálculo",
                    f"No se pudo procesar la entrada.\n\nDetalle: {e}",
                )
                self.status_bar.config(text=f"Error: {e}")

    def plot_function(self, func, a_str, b_str):
        try:
            self.reset_plot(clear_all=True)
            x_vals, y_vals, a_float, b_float = calc.generate_plot_data(
                func, a_str, b_str
            )
            p_style = self.style.PLOT_STYLE
            self.ax.plot(
                x_vals,
                y_vals,
                label=f"$f(x)={latex(func,mul_symbol='dot').replace('$','')}$",
                color=p_style["line"],
                linewidth=2,
            )
            self.ax.fill_between(
                x_vals,
                y_vals,
                where=((x_vals >= a_float) & (x_vals <= b_float)),
                color=p_style["fill"],
                alpha=0.4,
                label=f"Área de ${latex(a_str)}$ a ${latex(b_str)}$",
            )
            legend = self.ax.legend(
                facecolor=self.style.colors["SECONDARY_BG"],
                edgecolor=self.style.colors["SECONDARY_ACCENT"],
            )
            [t.set_color(self.style.colors["TEXT_COLOR"]) for t in legend.get_texts()]
            self.canvas.draw()
        except Exception as e:
            self.status_bar.config(text=f"Error al graficar: {e}")
            self.reset_plot(clear_all=True)
            self.canvas.draw()

    # --- MÉTODOS PARA TEMAS Y ESTILOS ---
    def _apply_theme(self, theme_name):
        self.style.set_theme(theme_name)
        colors, styles = self.style.colors, self.style
        self.root.config(bg=colors["BACKGROUND"])
        [f.config(bg=colors["BACKGROUND"]) for f in self.frames_to_style]
        self.func_entry.config(**styles.ENTRY_STYLE)
        self.lower_limit_entry.config(**styles.ENTRY_STYLE)
        self.upper_limit_entry.config(**styles.ENTRY_STYLE)
        self.calculate_button.config(**styles.BUTTON_STYLE)
        self.clear_button.config(**styles.BUTTON_STYLE)
        [b.config(**styles.BUTTON_STYLE) for b in self.calc_buttons]
        [self._update_widget_styles(w) for w in self.root.winfo_children()]
        self.result_label.config(**styles.RESULT_LABEL_STYLE)
        self.status_bar.config(**styles.LABEL_STYLE, relief=tk.SUNKEN)
        self._apply_theme_to_plot()

    def _update_widget_styles(self, parent):
        for c in parent.winfo_children():
            if c.winfo_class() == "Label":
                if c not in (self.status_bar, self.result_label):
                    c.config(**self.style.LABEL_STYLE)
            elif c.winfo_class() == "Frame":
                c.config(bg=self.style.colors["BACKGROUND"])
                self._update_widget_styles(c)

    def _apply_theme_to_plot(self):
        self.reset_plot()
        (
            all(
                (
                    self.func_entry.get(),
                    self.lower_limit_entry.get(),
                    self.upper_limit_entry.get(),
                )
            )
            and self.run_calculation(update_plot_only=True)
        ) or self.canvas.draw()

    def reset_plot(self, clear_all=True):
        if clear_all:
            self.ax.clear()
        p_style, f_config = self.style.PLOT_STYLE, {"family": self.style.FONT_FAMILY}
        self.ax.grid(True, linestyle="--", alpha=0.3, color=p_style["grid"])
        self.ax.axhline(0, color=p_style["grid"], linewidth=1)
        self.ax.axvline(0, color=p_style["grid"], linewidth=1)
        self.ax.set_title(
            "Gráfica de la Función", color=p_style["text"], fontdict=f_config
        )
        self.ax.set_xlabel("x", color=p_style["text"], fontdict=f_config)
        self.ax.set_ylabel("f(x)", color=p_style["text"], fontdict=f_config)

    # --- MÉTODOS AUXILIARES Y DE HISTORIAL/EXPORTACIÓN ---
    def export_to_pdf(self):
        if not self.last_calculation_data:
            messagebox.showwarning(
                "Nada que Exportar", "Por favor, realice un cálculo primero."
            )
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar reporte como...",
        )
        if not file_path:
            return
        try:
            self.status_bar.config(text="Generando PDF...")
            temp_image_path = os.path.join(os.path.dirname(__file__), "temp_graph.png")
            self.fig.savefig(temp_image_path, dpi=200, bbox_inches="tight")
            pdf = pdf_generator.create_integral_report(
                self.last_calculation_data, temp_image_path
            )
            pdf.output(file_path)
            os.remove(temp_image_path)
            self.status_bar.config(text="PDF generado exitosamente.")
            messagebox.showinfo(
                "Exportación Exitosa", f"El reporte ha sido guardado en:\n{file_path}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error de Exportación",
                f"No se pudo generar el archivo PDF.\n\nDetalle: {e}",
            )
            self.status_bar.config(text="Error al exportar PDF.")

    def _show_history_window(self):
        HistoryWindow(self.root, self, self.history)

    def load_from_history(self, history_entry):
        self.func_entry.delete(0, tk.END)
        self.lower_limit_entry.delete(0, tk.END)
        self.upper_limit_entry.delete(0, tk.END)
        self.func_entry.insert(0, history_entry["func_str"])
        self.lower_limit_entry.insert(0, history_entry["a_str"])
        self.upper_limit_entry.insert(0, history_entry["b_str"])
        self.run_calculation()

    def clear_all(self):
        self.func_entry.delete(0, tk.END)
        self.lower_limit_entry.delete(0, tk.END)
        self.upper_limit_entry.delete(0, tk.END)
        self.result_label.config(text="Ingrese una función para comenzar")
        self.status_bar.config(text="Listo")
        self.last_calculation_data = None
        self.reset_plot()
        self.canvas.draw()

    def insert_text(self, value):
        self.func_entry.insert(tk.INSERT, value)
        self.func_entry.focus()

    def show_about_info(self):
        messagebox.showinfo(
            "Acerca de Calculadora de Integrales",
            "Versión 2.2 (con PDF)\n\nDesarrollado por: [Jesel Moreno]\nProyecto de modificación de interfaz y funcionalidades.",
        )


# ===============================================================
# FIN DE LA CLASE PRINCIPAL DE LA APLICACIÓN
# ===============================================================
