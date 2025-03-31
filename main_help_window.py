import customtkinter as ctk
from tkinter import ttk

class MainHelpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajuda")
        self.geometry("450x300+300+300")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.create_putre_totem_tab()

    def create_putre_totem_tab(self):
        tab = ctk.CTkFrame(self.notebook)
        tab.pack(fill="both", expand=True)
        self.notebook.add(tab, text="Totem Putre")

        help_label = ctk.CTkLabel(tab, text="Hotkeys do Totem Putre:", font=ctk.CTkFont(weight="bold"))
        help_label.pack(pady=10)

        hotkeys_text = """
        Iniciar/Parar Ciclo: +
        Fechar App: Ctrl+Shift+Alt+Enter
        Aumentar Opacidade: Alt + (+)
        Diminuir Opacidade: Alt + (-)
        Arrastar Janela: Clique e arraste com o botão esquerdo do mouse
        """
        hotkeys_display = ctk.CTkLabel(tab, text=hotkeys_text, justify="left")
        hotkeys_display.pack(padx=20, pady=5, anchor="w")
