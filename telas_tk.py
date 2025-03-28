import customtkinter

class TelaBase(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

class TelaInicial(TelaBase):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        label = customtkinter.CTkLabel(self, text="Tela Inicial", font=customtkinter.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        pesquisar_button = customtkinter.CTkButton(self, text="Ir para Pesquisa de Item", command=controller.mostrar_tela_pesquisa_item)
        pesquisar_button.pack(pady=10)

        detalhe_button = customtkinter.CTkButton(self, text="Ir para Detalhe do Item (Exemplo)", command=lambda: controller.mostrar_tela_detalhe_item(123))
        detalhe_button.pack(pady=10)

class TelaPesquisaItem(TelaBase):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        label = customtkinter.CTkLabel(self, text="Tela de Pesquisa de Item", font=customtkinter.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        voltar_button = customtkinter.CTkButton(self, text="Voltar para Inicial", command=controller.mostrar_tela_inicial)
        voltar_button.pack(pady=10)

class TelaDetalheItem(TelaBase):
    def __init__(self, master, item_data, controller):
        super().__init__(master, controller)
        self.item_data = item_data

        label = customtkinter.CTkLabel(self, text=f"Detalhes do Item: {item_data.get('nome', 'Desconhecido')}", font=customtkinter.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        id_label = customtkinter.CTkLabel(self, text=f"ID: {item_data.get('id', 'N/A')}")
        id_label.pack(pady=5)

        voltar_button = customtkinter.CTkButton(self, text="Voltar para Inicial", command=controller.mostrar_tela_inicial)
        voltar_button.pack(pady=10)