# welcome_window.py (VERSIÓN CON LA CORRECCIÓN DEL ATRIBUTO 'EVAL')
import tkinter as tk


class WelcomeWindow(tk.Toplevel):
    """
    Ventana modal de bienvenida que proporciona instrucciones claras.
    """

    def __init__(self, master, style_manager):
        super().__init__(master)

        self.title("¡Bienvenido a la Calculadora de Integrales!")
        self.geometry("580x420")
        self.resizable(False, False)

        self.colors = style_manager.colors
        self.style = style_manager

        self.configure(bg=self.colors["BACKGROUND"])

        # --- LA LÍNEA CORREGIDA ---
        # Le pedimos al 'master' (la ventana principal 'root') que ejecute el comando
        # de centrado, especificando que la ventana a mover es 'self' (esta misma).
        self.master.eval(f"tk::PlaceWindow {str(self)} center")

        self._create_widgets()

        # Un pequeño extra: permitir cerrar con la tecla 'Escape'
        self.bind("<Escape>", lambda event: self.destroy())

        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def _create_widgets(self):
        """Crea y organiza todos los elementos de la ventana."""
        main_frame = tk.Frame(self, bg=self.colors["BACKGROUND"])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=20)

        header_label = tk.Label(
            main_frame,
            text="Calculadora de Integrales Definidas",
            font=(self.style.FONT_FAMILY, 16, "bold"),
            bg=self.colors["BACKGROUND"],
            fg=self.colors["PRIMARY_ACCENT"],
        )
        header_label.pack(pady=(0, 20))

        instructions_text = (
            "Esta aplicación calcula integrales definidas, grafica la función y exporta los resultados.\n\n"
            "• **Menú 'Archivo'**: Exporta el cálculo actual a PDF o cierra la aplicación.\n\n"
            "• **Menú 'Ver'**: Cambia entre tema Oscuro/Claro y consulta tu historial de cálculos.\n\n"
            "• **Formato de la Función**: Utiliza la sintaxis de Python. Ejemplos:\n"
            "  - Potencias: `x**2` o `x^3`\n"
            "  - Trigonométricas: `sin(x)`, `cos(x)`\n"
            "  - Raíz cuadrada: `sqrt(x)`\n"
            "  - Exponencial: `exp(x)`"
        )
        message_label = tk.Message(
            main_frame,
            text=instructions_text,
            font=(self.style.FONT_FAMILY, 11),
            bg=self.colors["BACKGROUND"],
            fg=self.colors["TEXT_COLOR"],
            width=500,
            justify=tk.LEFT,
        )
        message_label.pack(pady=(5, 20), fill=tk.X)

        close_button = tk.Button(
            main_frame, text="Comenzar", command=self.destroy, **self.style.BUTTON_STYLE
        )
        close_button.pack(pady=(10, 0))
