import tkinter as tk

class ClipboardMenu:
    def __init__(self, root, entrada):
        self.root = root
        self.entry_atual = None

        self.menu_popup = tk.Menu(root, tearoff=0)
        self.menu_popup.add_command(label="Copiar", command=self.copiar)
        self.menu_popup.add_command(label="Colar", command=self.colar)
        self.menu_popup.add_command(label="Recortar", command=self.recortar)

        entrada.bind("<Button-3>", self.mostrar_menu)

    def mostrar_menu(self, event):
        self.entry_atual = event.widget
        self.menu_popup.tk_popup(event.x_root, event.y_root)

    def copiar(self):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.entry_atual.selection_get())
        except tk.TclError:
            pass

    def colar(self):
        try:
            self.entry_atual.insert(tk.INSERT, self.root.clipboard_get())
        except tk.TclError:
            pass

    def recortar(self):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.entry_atual.selection_get())
            self.entry_atual.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
