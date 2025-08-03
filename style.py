# style.py (Versión Mejorada con Estilos TTK)
from tkinter import ttk

# Definimos las paletas de colores como diccionarios
THEMES = {
    "light": {
        "BACKGROUND": "#f8f9fa",
        "SECONDARY_BG": "#e9ecef",
        "TEXT_COLOR": "#212529",
        "PRIMARY_ACCENT": "#007bff",
        "SECONDARY_ACCENT": "#ced4da",
        "SUCCESS": "#28a745",
        "DANGER": "#dc3545",
        "WHITE": "#ffffff",
        "BUTTON_TEXT": "#ffffff",
        "BORDER": "#adb5bd",
    },
    "dark": {
        "BACKGROUND": "#2b2b2b",
        "SECONDARY_BG": "#3c3f41",  # Ligeramente más claro que el fondo para contraste
        "TEXT_COLOR": "#f1f1f1",
        "PRIMARY_ACCENT": "#007bff",
        "SECONDARY_ACCENT": "#6f7377",  # Un gris más notable
        "SUCCESS": "#1cc88a",
        "DANGER": "#e63946",
        "WHITE": "#ffffff",
        "BUTTON_TEXT": "#ffffff",
        "BORDER": "#888888",
    },
}


class Style:
    """
    Clase que gestiona y provee los diccionarios de estilo
    para la aplicación, basados en un tema activo.
    """

    def __init__(self, theme_name="dark"):
        self.set_theme(theme_name)

    def set_theme(self, theme_name):
        """Carga la paleta de colores y genera todos los estilos."""
        self.theme_name = theme_name
        self.colors = THEMES[theme_name]
        self.FONT_FAMILY = "Segoe UI"
        self._generate_styles()

    def _generate_styles(self):
        """
        Crea los diccionarios de estilo para widgets Tkinter y Matplotlib.
        """
        # Estilos Tkinter
        self.ENTRY_STYLE = {
            "font": (self.FONT_FAMILY, 12),
            "bg": self.colors["SECONDARY_BG"],
            "fg": self.colors["TEXT_COLOR"],
            "relief": "flat",
            "highlightthickness": 2,
            "highlightbackground": self.colors["SECONDARY_ACCENT"],
            "highlightcolor": self.colors["PRIMARY_ACCENT"],
            "insertbackground": self.colors["TEXT_COLOR"],
            "borderwidth": 0,  # Sin borde propio, confiamos en el highlight
        }
        self.BUTTON_STYLE = {
            "font": (self.FONT_FAMILY, 11, "bold"),
            "bg": self.colors["PRIMARY_ACCENT"],
            "fg": self.colors["BUTTON_TEXT"],
            "activebackground": self.colors["SUCCESS"],
            "activeforeground": self.colors["WHITE"],
            "relief": "raised",  # Un relieve sutil
            "borderwidth": 2,
            "padx": 10,
            "pady": 5,
            "cursor": "hand2",
        }
        self.LABEL_STYLE = {
            "bg": self.colors["BACKGROUND"],
            "fg": self.colors["TEXT_COLOR"],
            "font": (self.FONT_FAMILY, 12),
        }
        self.RESULT_LABEL_STYLE = {
            "bg": self.colors["BACKGROUND"],
            "fg": self.colors["TEXT_COLOR"],
            "font": (self.FONT_FAMILY, 14, "italic"),
            "justify": "left",
        }

        # Estilos para Matplotlib
        self.PLOT_STYLE = {
            "fig_bg": self.colors["BACKGROUND"],
            "axes_bg": self.colors["SECONDARY_BG"],
            "text": self.colors["TEXT_COLOR"],
            "grid": self.colors["SECONDARY_ACCENT"],
            "line": "#00c0ff",
            "fill": "#e63946",  # Color de relleno más vibrante
        }

    def configure_ttk_styles(self):
        """
        Configura los estilos para los widgets TTK de forma centralizada.
        Esta es la forma correcta de dar estilo a ttk.Separator y ttk.Progressbar.
        """
        style = ttk.Style()
        style.theme_use("clam")  # 'clam' permite una mayor personalización

        # Estilo para Separadores
        separator_color = self.colors["SECONDARY_ACCENT"]
        if self.theme_name == "light":
            # En modo claro, el separador se "oculta" teniendo el color del fondo
            separator_color = self.colors["BACKGROUND"]

        style.configure("TSeparator", background=separator_color)

        # Estilo para la Barra de Progreso
        style.configure(
            "TProgressbar",
            thickness=20,
            background=self.colors["SUCCESS"],
            troughcolor=self.colors["SECONDARY_BG"],
        )
