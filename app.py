# app.py (VERSIÓN FINAL CON ALERTAS DE VALIDACIÓN RESTAURADAS)
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
    ttk,
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import latex
import os

import pdf_generator
from style import Style
import calculator_logic as calc
from history_window import HistoryWindow
from tooltip import ToolTip


class IntegralCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.style = Style("dark")

        self.root.title("Calculadora de Integrales Definidas")
        self.root.geometry("1200x800")

        self.calc_buttons = []
        self.icons = {}
        self.history = []
        self.last_calculation_data = None
        self.latex_photo = None

        self._load_icons()
        self._create_menu()
        self._create_widgets()
        self._create_bottom_bar()

        self._apply_theme(self.style.theme_name)

        self.reset_plot()
        self.canvas.draw()

    # --- Creación de Widgets (sin cambios) ---
    def _create_widgets(self):
        main_container = Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        main_container.columnconfigure(0, weight=1, uniform="group1")
        main_container.columnconfigure(1, weight=2, uniform="group1")
        main_container.rowconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        self.top_left_frame = Frame(main_container)
        self.top_left_frame.grid(
            row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 5)
        )
        self.bottom_left_frame = Frame(main_container)
        self.bottom_left_frame.grid(
            row=1, column=0, sticky="nsew", padx=(0, 10), pady=(5, 0)
        )
        self.top_right_frame = Frame(main_container)
        self.top_right_frame.grid(
            row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 5)
        )
        self.latex_frame = Frame(main_container)
        self.latex_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(5, 0))
        self.latex_frame.pack_propagate(False)
        input_frame = Frame(self.top_left_frame)
        input_frame.pack(expand=True, padx=10, pady=10)
        self.label_func = Label(input_frame, text="f(x):")
        self.label_func.grid(row=0, column=0, sticky="w", pady=(10, 2), padx=5)
        self.func_entry = Entry(input_frame, width=30)
        self.func_entry.grid(row=1, column=0, sticky="ew", ipady=4)
        ToolTip(self.func_entry, "Ingrese la función (ej. x**2).")
        self.label_a = Label(input_frame, text="Límite inferior (a):")
        self.label_a.grid(row=2, column=0, sticky="w", pady=(10, 2), padx=5)
        self.lower_limit_entry = Entry(input_frame, width=30)
        self.lower_limit_entry.grid(row=3, column=0, sticky="ew", ipady=4)
        ToolTip(self.lower_limit_entry, "Valor inicial para la integración.")
        self.label_b = Label(input_frame, text="Límite superior (b):")
        self.label_b.grid(row=4, column=0, sticky="w", pady=(10, 2), padx=5)
        self.upper_limit_entry = Entry(input_frame, width=30)
        self.upper_limit_entry.grid(row=5, column=0, sticky="ew", ipady=4)
        ToolTip(self.upper_limit_entry, "Valor final para la integración.")
        action_frame = Frame(input_frame)
        action_frame.grid(row=6, column=0, pady=20, sticky="e")
        self.calculate_button = Button(
            action_frame,
            text="Calcular",
            image=self.icons.get("calculate"),
            compound=tk.LEFT,
            command=self.run_calculation,
        )
        self.calculate_button.pack(side="left", padx=5)
        ToolTip(self.calculate_button, "Realiza el cálculo.")
        self.clear_button = Button(
            action_frame,
            text="Limpiar",
            image=self.icons.get("clear"),
            compound=tk.LEFT,
            command=self.clear_all,
        )
        self.clear_button.pack(side="left", padx=5)
        ToolTip(self.clear_button, "Borra todas las entradas.")
        keypad_frame = Frame(self.bottom_left_frame)
        keypad_frame.pack(pady=10)
        self._create_calculator_buttons(keypad_frame)
        self.result_label = Label(
            self.bottom_left_frame, text="Esperando cálculo...", wraplength=350
        )
        self.result_label.pack(pady=(10, 20), expand=True)
        self._create_plot_area(self.top_right_frame)
        self.latex_image_label = Label(self.latex_frame)
        self.latex_image_label.pack(expand=True)
        self.v_separator = ttk.Separator(
            main_container, orient="vertical", style="TSeparator"
        )
        self.v_separator.grid(row=0, column=0, rowspan=2, sticky="nse")
        self.h_separator = ttk.Separator(
            main_container, orient="horizontal", style="TSeparator"
        )
        self.h_separator.grid(row=0, column=0, columnspan=2, sticky="sew")

    # --- LÓGICA DE CÁLCULO Y VALIDACIÓN (AQUÍ ESTÁN LOS CAMBIOS) ---

    def run_calculation(self):
        """
        ### MÉTODO CORREGIDO ###
        Valida las entradas ANTES de iniciar cualquier cálculo o animación.
        Si algo falta, muestra una alerta y detiene la ejecución.
        """
        func_str = self.func_entry.get()
        a_str = self.lower_limit_entry.get()
        b_str = self.upper_limit_entry.get()

        if not all([func_str, a_str, b_str]):
            # ¡La alerta que extrañábamos ha vuelto!
            messagebox.showwarning(
                "Campos Incompletos",
                "Por favor, complete todos los campos (función y límites) antes de calcular.",
            )
            return  # Detiene el proceso aquí si faltan datos.

        # Si la validación es exitosa, ahora sí procedemos con la animación.
        self._animate_progress()

    def _animate_progress(self, step=0):
        """Inicia y controla la animación de la barra de progreso."""
        if step == 0:
            self.progress_label.config(text="Calculando...")
            self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            self.progress_bar["value"] = 0
        if step <= 100:
            self.progress_bar["value"] = step
            self.root.after(5, self._animate_progress, step + 4)
        else:
            self._perform_calculation()
            self.root.after(
                1500,
                lambda: (
                    self.progress_bar.pack_forget(),
                    self.progress_label.config(text="Listo"),
                ),
            )

    def _perform_calculation(self, update_plot_only=False):
        """
        ### MÉTODO SIMPLIFICADO ###
        Realiza el cálculo asumiendo que las entradas ya fueron validadas.
        """
        try:
            # Obtiene los datos de nuevo (no pasa nada, es rápido).
            func_str, a_str, b_str = (
                self.func_entry.get(),
                self.lower_limit_entry.get(),
                self.upper_limit_entry.get(),
            )
            # La validación de campos vacíos ya no es necesaria aquí.

            func = calc.parse_expression(func_str)
            if not update_plot_only:
                res_def, res_indef = calc.calculate_definite_integral(
                    func, a_str, b_str
                ), calc.calculate_indefinite_integral(func)
                res_def_float = float(res_def)
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
                self.result_label.config(
                    text=f"∫ de {a_str} a {b_str} de f(x) dx ≈ {res_def_float:.4f}\nIntegral indefinida: {self.last_calculation_data['result_indef_latex']}"
                )

            self._update_latex_display(func, a_str, b_str)
            self.plot_function(func, a_str, b_str)

            if not update_plot_only:
                self.progress_label.config(text="Cálculo completado.")
        except Exception as e:
            if not update_plot_only:
                messagebox.showerror(
                    "Error de Cálculo",
                    f"No se pudo procesar la entrada.\n\nDetalle: {e}",
                )
                self.progress_label.config(text="Error en el cálculo.")

    # --- Resto de la clase (sin cambios, todo lo demás está perfecto) ---

    def _create_bottom_bar(self):
        self.bottom_bar_frame = Frame(self.root, height=30)
        self.bottom_bar_frame.pack(side=tk.BOTTOM, fill=tk.X, ipady=2)
        self.bottom_bar_frame.pack_propagate(False)
        self.progress_bar = ttk.Progressbar(
            self.bottom_bar_frame,
            orient="horizontal",
            mode="determinate",
            style="TProgressbar",
        )
        self.progress_label = Label(self.bottom_bar_frame, text="Listo")
        self.progress_label.pack(side=tk.LEFT, padx=10)

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
        except:
            self.icons.update({"calculate": None, "clear": None})

    def _create_menu(self):
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar a PDF...", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
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
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self.show_about_info)

    def _create_plot_area(self, parent_frame):
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def _create_calculator_buttons(self, parent):
        buttons = [
            ["sin(", "cos(", "tan(", "^", "sqrt("],
            ["7", "8", "9", "/", "exp("],
            ["4", "5", "6", "*", "ln("],
            ["1", "2", "3", "-", "("],
            ["0", ".", "+", "e", ")"],
        ]
        for i, r in enumerate(buttons):
            for j, v in enumerate(r):
                btn = Button(
                    parent, text=v, width=5, command=lambda v=v: self.insert_text(v)
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.calc_buttons.append(btn)

    def _apply_theme(self, theme_name):
        self.style.set_theme(theme_name)
        styles = self.style
        colors = self.style.colors
        self.style.configure_ttk_styles()
        self.root.config(bg=colors["BACKGROUND"])

        def style_recursive(widget):
            if isinstance(widget, (Frame, ttk.Frame)):
                if widget not in [self.bottom_bar_frame, self.latex_frame]:
                    widget.config(bg=colors["BACKGROUND"])
            for child in widget.winfo_children():
                style_recursive(child)

        style_recursive(self.root)
        self.func_entry.config(**styles.ENTRY_STYLE)
        self.lower_limit_entry.config(**styles.ENTRY_STYLE)
        self.upper_limit_entry.config(**styles.ENTRY_STYLE)
        self.calculate_button.config(**styles.BUTTON_STYLE)
        self.clear_button.config(**styles.BUTTON_STYLE)
        for btn in self.calc_buttons:
            btn.config(**styles.BUTTON_STYLE)
        self.label_func.config(**styles.LABEL_STYLE)
        self.label_a.config(**styles.LABEL_STYLE)
        self.label_b.config(**styles.LABEL_STYLE)
        self.result_label.config(**styles.RESULT_LABEL_STYLE)
        self.bottom_bar_frame.config(bg=colors["SECONDARY_BG"])
        self.progress_label.config(
            bg=colors["SECONDARY_BG"],
            fg=colors["TEXT_COLOR"],
            font=(self.style.FONT_FAMILY, 10),
        )
        self.latex_frame.config(bg=colors["SECONDARY_BG"])
        self.latex_image_label.config(bg=colors["SECONDARY_BG"])
        self._apply_theme_to_plot()

    def _apply_theme_to_plot(self):
        self.reset_plot()
        if all(
            (
                self.func_entry.get(),
                self.lower_limit_entry.get(),
                self.upper_limit_entry.get(),
            )
        ):
            self._perform_calculation(update_plot_only=True)
        else:
            self.canvas.draw()

    def _show_history_window(self):
        HistoryWindow(self.root, self, self.history)

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
            self.progress_label.config(text=f"Error al graficar: {e}")
            self.reset_plot(clear_all=True)
            self.canvas.draw()

    def _update_latex_display(self, func, a_str, b_str, force_color=None):
        try:
            if not self.last_calculation_data:
                return None
            res_def_float = float(self.last_calculation_data["result_def"])
            latex_str = f"$\\int_{{{latex(a_str)}}}^{{{latex(b_str)}}} {latex(func)}\\,dx = {res_def_float:.4f}$"
            text_color = force_color if force_color else self.style.colors["TEXT_COLOR"]
            fig = Figure(figsize=(5, 1), dpi=120)
            fig.patch.set_facecolor("none")
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor("none")
            ax.text(
                0.5,
                0.5,
                latex_str,
                ha="center",
                va="center",
                fontsize=22,
                color=text_color,
            )
            ax.axis("off")
            temp_dir = os.path.join(os.path.dirname(__file__), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            latex_image_path = os.path.join(temp_dir, "temp_latex_formula.png")
            fig.savefig(
                latex_image_path,
                format="png",
                bbox_inches="tight",
                pad_inches=0.1,
                transparent=True,
            )
            if not force_color:
                self.latex_photo = PhotoImage(file=latex_image_path)
                self.latex_image_label.config(image=self.latex_photo)
            return latex_image_path
        except Exception:
            if not force_color:
                self.latex_image_label.config(image="")
            return None

    def clear_all(self):
        self.func_entry.delete(0, tk.END)
        self.lower_limit_entry.delete(0, tk.END)
        self.upper_limit_entry.delete(0, tk.END)
        self.result_label.config(text="Esperando cálculo...")
        self.progress_label.config(text="Listo")
        self.last_calculation_data = None
        if self.latex_photo:
            self.latex_image_label.config(image="")
            self.latex_photo = None
        self.reset_plot()
        self.canvas.draw()

    def reset_plot(self, clear_all=True):
        if clear_all:
            self.ax.clear()
        p_style = self.style.PLOT_STYLE
        f_config = {"family": self.style.FONT_FAMILY}
        self.fig.set_facecolor(p_style["fig_bg"])
        self.ax.set_facecolor(p_style["axes_bg"])
        self.ax.grid(True, linestyle="--", alpha=0.3, color=p_style["grid"])
        self.ax.axhline(0, color=p_style["grid"], linewidth=1)
        self.ax.axvline(0, color=p_style["grid"], linewidth=1)
        self.ax.set_title(
            "Gráfica de la Función", color=p_style["text"], fontdict=f_config
        )
        self.ax.set_xlabel("x", color=p_style["text"], fontdict=f_config)
        self.ax.set_ylabel("f(x)", color=p_style["text"], fontdict=f_config)
        self.ax.tick_params(axis="x", colors=p_style["text"])
        self.ax.tick_params(axis="y", colors=p_style["text"])
        self.ax.spines["left"].set_color(p_style["text"])
        self.ax.spines["right"].set_color(p_style["text"])
        self.ax.spines["top"].set_color(p_style["text"])
        self.ax.spines["bottom"].set_color(p_style["text"])

    def export_to_pdf(self):
        if not self.last_calculation_data:
            messagebox.showwarning("Nada que Exportar", "Realice un cálculo primero.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf"), ("Todos", "*.*")],
            title="Guardar...",
        )
        if not file_path:
            return
        try:
            self.progress_label.config(text="Generando PDF...")
            temp_dir = os.path.join(os.path.dirname(__file__), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_graph_path = os.path.join(temp_dir, "temp_graph.png")
            self.fig.savefig(temp_graph_path, dpi=200, bbox_inches="tight")
            temp_latex_path = self._update_latex_display(
                calc.parse_expression(self.last_calculation_data["func_str"]),
                self.last_calculation_data["a_str"],
                self.last_calculation_data["b_str"],
                force_color="black",
            )
            if temp_latex_path is None:
                raise Exception("No se pudo generar la imagen de LaTeX.")
            pdf = pdf_generator.create_integral_report(
                self.last_calculation_data, temp_graph_path, temp_latex_path
            )
            pdf.output(file_path)
            if os.path.exists(temp_graph_path):
                os.remove(temp_graph_path)
            if os.path.exists(temp_latex_path):
                os.remove(temp_latex_path)
            self.progress_label.config(text="PDF generado.")
            messagebox.showinfo("Éxito", f"Reporte guardado en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar PDF.\nDetalle: {e}")
            self.progress_label.config(text="Error.")

    def load_from_history(self, history_entry):
        self.func_entry.delete(0, tk.END)
        self.lower_limit_entry.delete(0, tk.END)
        self.upper_limit_entry.delete(0, tk.END)
        self.func_entry.insert(0, history_entry["func_str"])
        self.lower_limit_entry.insert(0, history_entry["a_str"])
        self.upper_limit_entry.insert(0, history_entry["b_str"])
        self.run_calculation()

    def insert_text(self, value):
        focused_widget = self.root.focus_get()
        if isinstance(focused_widget, Entry):
            focused_widget.insert(tk.INSERT, value)
        else:
            self.func_entry.insert(tk.INSERT, value)
            self.func_entry.focus()

    def show_about_info(self):
        messagebox.showinfo(
            "Acerca de...",
            "Calculadora de Integrales v2.7 \n\nDesarrollado por Jesel Moreno.",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = IntegralCalculatorApp(root)
    root.mainloop()
