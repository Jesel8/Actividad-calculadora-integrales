# history_window.py (Versión Mejorada con Leyenda y Estilo de Tabla)
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

        self.title("Historial y Memoria de Cálculos")
        self.geometry("650x450")  # Un poco más ancha para que no se corte el texto
        self.resizable(
            True, True
        )  # Permitir redimensionar es bueno para historiales largos

        # --- MEJORA: Obtenemos el estilo y los colores desde la app principal ---
        self.style = self.app.style
        self.colors = self.style.colors

        self.configure(bg=self.colors["BACKGROUND"])

        self._create_widgets()
        self._populate_tree()

        # Configuración estándar de la ventana modal
        self.transient(master)
        self.grab_set()

    def _create_widgets(self):
        frame = tk.Frame(self, bg=self.colors["BACKGROUND"])
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        # --- MEJORA: Se añade estilo al Treeview para que coincida con el tema ---
        # El estilo de los widgets ttk se maneja de forma centralizada con ttk.Style()
        ttk_style = ttk.Style()

        # Configuramos los colores de las filas, el texto y la selección
        ttk_style.configure(
            "History.Treeview",
            background=self.colors["SECONDARY_BG"],
            foreground=self.colors["TEXT_COLOR"],
            fieldbackground=self.colors["SECONDARY_BG"],
            rowheight=25,  # Un poco más de espacio por fila
            font=(self.style.FONT_FAMILY, 10),
        )
        # Resaltamos el color de la fila seleccionada
        ttk_style.map(
            "History.Treeview", background=[("selected", self.colors["PRIMARY_ACCENT"])]
        )

        # Configuramos los encabezados de la tabla para que sean más visibles
        ttk_style.configure(
            "History.Treeview.Heading",
            background=self.colors["PRIMARY_ACCENT"],
            foreground=self.colors["BUTTON_TEXT"],
            font=(self.style.FONT_FAMILY, 11, "bold"),
            relief="flat",
        )

        columns = ("function", "limits", "result")
        # Aplicamos el estilo creado al Treeview
        self.tree = ttk.Treeview(
            frame, columns=columns, show="headings", style="History.Treeview"
        )

        self.tree.heading("function", text="Función f(x)")
        self.tree.heading("limits", text="Límites [a, b]")
        self.tree.heading("result", text="Resultado")

        self.tree.column("function", width=280)
        self.tree.column("limits", width=120, anchor=tk.CENTER)
        self.tree.column("result", width=150, anchor=tk.CENTER)

        self.tree.bind("<Double-1>", self._on_item_double_click)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # --- MEJORA: Creación de la leyenda/etiqueta instructiva ---
        info_label = tk.Label(
            frame,
            text="MEMORIA: Haz doble clic en una fila para cargar el cálculo.",
            font=(self.style.FONT_FAMILY, 10, "italic"),
            bg=self.colors["BACKGROUND"],
            fg=self.colors["TEXT_COLOR"],
            pady=5,
        )

        # --- Posicionamiento de los widgets en el grid ---
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        # La nueva etiqueta va debajo de la tabla
        info_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Hacemos que la tabla se expanda para llenar el espacio disponible
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def _populate_tree(self):
        """Llena la tabla con los datos del historial."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in self.history:
            limits_str = f"[{entry['a_str']}, {entry['b_str']}]"
            values = (entry["func_str"], limits_str, entry["result_def"])
            self.tree.insert("", tk.END, values=values)

    def _on_item_double_click(self, event):
        """Carga la operación en la ventana principal al hacer doble clic."""
        if not self.tree.selection():
            return

        item_id = self.tree.selection()[0]
        # Obtenemos el índice de la fila clickeada para encontrarla en la lista original del historial
        item_index = self.tree.index(item_id)

        # El historial en la tabla puede estar ordenado de forma diferente al original,
        # así que nos aseguramos de tomar el dato correcto.
        # En nuestro caso, como no hay ordenación, es directo.
        selected_history_entry = self.history[item_index]

        # Llamamos al método de la app principal para cargar los datos
        self.app.load_from_history(selected_history_entry)

        # Cerramos la ventana de historial
        self.destroy()
