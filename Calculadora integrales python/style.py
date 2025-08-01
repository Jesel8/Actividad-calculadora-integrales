# Contiene todas las definiciones de estilo de la aplicación.

class Style:
    # Colores base (aquí haremos el cambio de esquema más adelante)
    PRIMARY = "#e63946"
    SECONDARY = "#f1faee" 
    BACKGROUND = "#f8f9fa"
    TEXT_COLOR = "#1d3557"
    ACCENT = "#457b9d"

    # Estilos para widgets
    FONT_FAMILY = "Segoe UI"
    
    ENTRY_STYLE = {
        "font": (FONT_FAMILY, 12),
        "bg": "#e9ecef",
        "fg": TEXT_COLOR,
        "relief": "flat",
        "highlightthickness": 1,
        "highlightbackground": "#ced4da",
        "highlightcolor": PRIMARY
    }

    BUTTON_STYLE = {
        "font": (FONT_FAMILY, 12),
        "bg": PRIMARY,
        "fg": SECONDARY,
        "activebackground": "#d62828", # Un rojo un poco más oscuro al presionar
        "activeforeground": SECONDARY,
        "relief": "flat",
        "padx": 10,
        "pady": 5
    }