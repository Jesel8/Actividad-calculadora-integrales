# style.py (Versión con Temas Dinámicos)

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
    },
    "dark": {
        "BACKGROUND": "#2b2b2b",  # fondo principal
        "SECONDARY_BG": "#4a4a4a",  # fondo de secciones secundarias (como el recuadro de latex)
        "TEXT_COLOR": "#f1f1f1",  # texto claro
        "PRIMARY_ACCENT": "#00aaff",  # línea azul brillante
        "SECONDARY_ACCENT": "#888888",  # bordes / grid
        "SUCCESS": "#1cc88a",  # hover o success
        "DANGER": "#e63946",
        "WHITE": "#ffffff",
        "BUTTON_TEXT": "#ffffff",
    },
}


class Style:
    """
    Clase que gestiona y provee los diccionarios de estilo
    para la aplicación, basados en un tema activo.
    """

    def __init__(self, theme_name="dark"):  # Modo oscuro por defecto
        self.set_theme(theme_name)

    def set_theme(self, theme_name):
        """Carga la paleta de colores del tema especificado."""
        self.theme_name = theme_name
        self.colors = THEMES[theme_name]
        self.FONT_FAMILY = "Segoe UI"
        self._generate_styles()

    def _generate_styles(self):
        """
        Crea los diccionarios de estilo para los widgets de Tkinter y Matplotlib
        usando la paleta de colores actual.
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
        }
        self.BUTTON_STYLE = {
            "font": (self.FONT_FAMILY, 11, "bold"),
            "bg": self.colors["PRIMARY_ACCENT"],
            "fg": self.colors["BUTTON_TEXT"],
            "activebackground": self.colors["SUCCESS"],
            "activeforeground": self.colors["WHITE"],
            "relief": "flat",
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

        # Colores para Matplotlib (lo pasaremos como un diccionario)
        self.PLOT_STYLE = {
            "fig_bg": self.colors["BACKGROUND"],
            "axes_bg": self.colors["SECONDARY_BG"],
            "text": self.colors["TEXT_COLOR"],
            "grid": self.colors["SECONDARY_ACCENT"],
            "line": "#00c0ff",  # Azul fuerte
            "fill": "#c10000",  # Rojo vino / rojo oscuro para el área
        }
