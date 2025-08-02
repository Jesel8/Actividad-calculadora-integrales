# history_window.py (Versión Corregida para coincidir con la app principal)
import tkinter as tk
from tkinter import ttk  # Necesitamos ttk para el widget Treeview


class HistoryWindow(tk.Toplevel):
    """
    Una nueva ventana (Toplevel) que muestra el historial de cálculos
    en una tabla (Treeview) y permite cargar cálculos anteriores.
    """

    def __init__(self, master, app_instance, history_data):
        super().__init__(master)

        self.app = app_instance
        self.history = history_data

        self.title("Historial de Cálculos")
        self.geometry("600x400")
        self.resizable(False, False)

        theme_colors = self.app.style.colors
        self.configure(bg=theme_colors["BACKGROUND"])

        self._create_widgets()
        self._populate_tree()

        self.transient(master)
        self.grab_set()

    def _create_widgets(self):
        frame = tk.Frame(self, bg=self.app.style.colors["BACKGROUND"])
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        columns = ("function", "limits", "result")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        self.tree.heading("function", text="Función f(x)")
        self.tree.heading("limits", text="Límites [a, b]")
        self.tree.heading("result", text="Resultado")

        self.tree.column("function", width=250)
        self.tree.column("limits", width=100, anchor=tk.CENTER)
        self.tree.column("result", width=150, anchor=tk.CENTER)

        self.tree.bind("<Double-1>", self._on_item_double_click)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    # --- INICIO DE LA CORRECCIÓN ---
    def _populate_tree(self):
        """Llena la tabla con los datos del historial usando las claves correctas."""
        # Borramos los datos antiguos para evitar duplicados si la ventana se abre más de una vez
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Iteramos a través del historial y usamos las nuevas claves
        for entry in self.history:
            # ### CAMBIO: Se usan las nuevas claves 'a_str' y 'b_str' que definimos en app.py.
            limits_str = f"[{entry['a_str']}, {entry['b_str']}]"

            # ### CAMBIO: Se usan las claves 'func_str' y 'result_def'.
            values = (entry["func_str"], limits_str, entry["result_def"])

            # Insertamos la fila en la tabla
            self.tree.insert("", tk.END, values=values)

    # --- FIN DE LA CORRECCIÓN ---

    def _on_item_double_click(self, event):
        """
        Se ejecuta cuando un usuario hace doble clic en una fila.
        Carga la operación en la ventana principal.
        """
        # Se añade una comprobación para evitar un error si el usuario hace clic en una zona vacía
        if not self.tree.selection():
            return

        item_id = self.tree.selection()[0]
        item_index = self.tree.index(item_id)

        selected_history_entry = self.history[item_index]

        # El método load_from_history en app.py ya espera un diccionario con las claves nuevas,
        # así que esta llamada ahora es correcta.
        self.app.load_from_history(selected_history_entry)

        self.destroy()
