# tooltip.py
import tkinter as tk


class ToolTip(object):
    """
    Crea un tooltip (mensaje de ayuda emergente) para un widget de tkinter.
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Asocia los eventos de entrar y salir del widget a las funciones de mostrar/ocultar.
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Muestra el tooltip cerca del cursor."""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Crea una nueva ventana Toplevel (sin bordes ni título)
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Estilo del tooltip
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        """Oculta y destruye la ventana del tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None
