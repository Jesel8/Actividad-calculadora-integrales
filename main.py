import tkinter as tk
from app import IntegralCalculatorApp

if __name__ == "__main__":
    # Creamos la ventana principal
    root = tk.Tk()
    
    # Creamos una instancia de nuestra aplicación
    app = IntegralCalculatorApp(root)
    
    # Iniciamos el bucle principal de la aplicación
    root.mainloop()