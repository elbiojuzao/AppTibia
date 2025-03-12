import tkinter as tk
from tkinter import ttk
import requests

class InfoWorldWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Informações do Mundo")

        # Dropdown com nomes de servidores
        self.servers = self.fetch_server_names()
        self.server_var = tk.StringVar(root)
        self.server_var.set(self.servers[0])
        self.server_dropdown = ttk.Combobox(root, textvariable=self.server_var, values=self.servers, state="readonly")
        self.server_dropdown.pack(pady=10)
        self.server_dropdown.bind("<<ComboboxSelected>>", self.update_world_info)

        # Labels para informações do mundo
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack()
        self.players_online_label = ttk.Label(root, text="")
        self.players_online_label.pack()
        self.location_label = ttk.Label(root, text="")
        self.location_label.pack()
        self.pvp_type_label = ttk.Label(root, text="")
        self.pvp_type_label.pack()
        self.quest_titles_label = ttk.Label(root, text="")
        self.quest_titles_label.pack()
        self.battleye_label = ttk.Label(root, text="")
        self.battleye_label.pack()

        # Botões "Highscores" e "Character"
        self.highscores_button = ttk.Button(root, text="Highscores", command=self.open_highscores)
        self.highscores_button.pack(pady=5)

        # Frame para o botão Character e o TextBox
        self.character_frame = ttk.Frame(root)
        self.character_frame.pack(pady=5, fill="x")

        self.character_button = ttk.Button(self.character_frame, text="Character", command=self.open_character)
        self.character_button.pack(side="left")

        self.character_name_entry = ttk.Entry(self.character_frame)
        self.character_name_entry.pack(side="left", padx=5)

        self.update_world_info(None)  # Carrega informações do primeiro servidor ao iniciar

    def fetch_server_names(self):
        url = "https://dev.tibiadata.com/v4/worlds"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return [world["name"] for world in data["worlds"]["allworlds"]["world"]] # Correção aqui
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar nomes de servidores: {e}")
            return []

    def update_world_info(self, event):
        server_name = self.server_var.get()
        url = f"https://dev.tibiadata.com/v4/world/{server_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            world = data["worlds"]["world"]
            self.status_label.config(text=f"Status: {world['status']}")
            self.players_online_label.config(text=f"Players Online: {world['players_online']}")
            self.location_label.config(text=f"Location: {world['location']}")
            self.pvp_type_label.config(text=f"PVP Type: {world['pvp_type']}")
            self.quest_titles_label.config(text=f"Quest Titles: {', '.join(world['world_quest_titles']) if world['world_quest_titles'] else 'None'}")
            self.battleye_label.config(text=f"Battleye Protected: {'Yes' if world['battleye_protected'] else 'No'}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar informações do servidor: {e}")
            self.status_label.config(text="Erro ao buscar informações.")
            self.players_online_label.config(text="")
            self.location_label.config(text="")
            self.pvp_type_label.config(text="")
            self.quest_titles_label.config(text="")
            self.battleye_label.config(text="")

    def open_highscores(self):
        print("Abrindo Highscores...")

    def open_character(self):
        character_name = self.character_name_entry.get()
        print(f"Abrindo Character: {character_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InfoWorldWindow(root)
    root.mainloop()