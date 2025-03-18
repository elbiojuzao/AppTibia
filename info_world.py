import tkinter as tk
from tkinter import ttk
import requests
import json
import os

class InfoWorldWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Informações do Mundo")

        # Carrega o último servidor selecionado
        self.last_selected_server = self.load_last_selected_server()

        # Dropdown com nomes de servidores
        self.servers = self.fetch_server_names()
        self.server_var = tk.StringVar(root)
        if self.last_selected_server and self.last_selected_server in self.servers:
            self.server_var.set(self.last_selected_server)
        else:
            self.server_var.set("Antica")
        self.server_dropdown = ttk.Combobox(root, textvariable=self.server_var, values=self.servers, state="readonly")
        self.server_dropdown.pack(pady=10)
        self.server_dropdown.bind("<<ComboboxSelected>>", self.update_world_info)

        # Frame para status com bolinha
        self.status_frame = ttk.Frame(root)
        self.status_frame.pack()
        self.status_label = ttk.Label(self.status_frame, text="Status:", font=("TkDefaultFont", 10, "bold"))
        self.status_label.pack(side=tk.LEFT)
        self.status_canvas = tk.Canvas(self.status_frame, width=10, height=10, highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=5)
        self.status_text = ttk.Label(self.status_frame, text="")
        self.status_text.pack(side=tk.LEFT)

        # Frame para players online
        self.players_online_frame = ttk.Frame(root)
        self.players_online_frame.pack()
        self.players_online_label = ttk.Label(self.players_online_frame, text="Players Online:", font=("TkDefaultFont", 10, "bold"))
        self.players_online_label.pack(side=tk.LEFT)
        self.players_online_text = ttk.Label(self.players_online_frame, text="")
        self.players_online_text.pack(side=tk.LEFT)

        # Frame para localização
        self.location_frame = ttk.Frame(root)
        self.location_frame.pack()
        self.location_label = ttk.Label(self.location_frame, text="Location:", font=("TkDefaultFont", 10, "bold"))
        self.location_label.pack(side=tk.LEFT)
        self.location_text = ttk.Label(self.location_frame, text="")
        self.location_text.pack(side=tk.LEFT)

        # Frame para tipo de PVP
        self.pvp_type_frame = ttk.Frame(root)
        self.pvp_type_frame.pack()
        self.pvp_type_label = ttk.Label(self.pvp_type_frame, text="PVP Type:", font=("TkDefaultFont", 10, "bold"))
        self.pvp_type_label.pack(side=tk.LEFT)
        self.pvp_type_text = ttk.Label(self.pvp_type_frame, text="")
        self.pvp_type_text.pack(side=tk.LEFT)

        # Frame para títulos de quests
        self.quest_titles_label = ttk.Label(root, text="Quest Titles:", justify="left", anchor="nw", font=("TkDefaultFont", 10, "bold"))
        self.quest_titles_label.pack()
        self.quest_titles_text = ttk.Label(root, text="", justify="left", anchor="nw")
        self.quest_titles_text.pack()

        # Frame para BattlEye com bolinha
        self.battleye_frame = ttk.Frame(root)
        self.battleye_frame.pack()
        self.battleye_label = ttk.Label(self.battleye_frame, text="BattlEye Protected:", font=("TkDefaultFont", 10, "bold"))
        self.battleye_label.pack(side=tk.LEFT)
        self.battleye_canvas = tk.Canvas(self.battleye_frame, width=10, height=10, highlightthickness=0)
        self.battleye_canvas.pack(side=tk.LEFT, padx=5)
        self.battleye_text = ttk.Label(self.battleye_frame, text="")
        self.battleye_text.pack(side=tk.LEFT)

        # Botões "Highscores"
        self.highscores_button = ttk.Button(root, text="Highscores", command=self.open_highscores)
        self.highscores_button.pack(pady=5)

        self.update_world_info(None)  # Carrega informações do primeiro servidor ao iniciar

        # Salva o último servidor selecionado ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def fetch_server_names(self):
        url = "https://api.tibiadata.com/v4/worlds"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return [world["name"] for world in data["worlds"]["regular_worlds"]]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar nomes de servidores: {e}")
            return []

    def update_world_info(self, event):
        server_name = self.server_var.get()
        self.save_last_selected_server(server_name)  # Salva o servidor selecionado
        url = f"https://api.tibiadata.com/v4/world/{server_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            world = data["world"]

            # Atualiza o status com a bolinha
            status = world['status']
            self.status_text.config(text=status)
            self.draw_circle(self.status_canvas, "green" if status == "online" else "red")

            self.players_online_text.config(text=f"{world['players_online']}")
            self.location_text.config(text=f"{world['location']}")
            self.pvp_type_text.config(text=f"{world['pvp_type']}")

            # Formata os títulos de quests
            quest_titles = world['world_quest_titles']
            if quest_titles:
                formatted_titles = "\n".join([f"  - {title}" for title in quest_titles])
            else:
                formatted_titles = "None"
            self.quest_titles_text.config(text=f"{formatted_titles}")

            # Atualiza o BattlEye com a bolinha
            battleye_protected = world['battleye_protected']
            battleye_date = world.get('battleye_date') # Obtém a data do BattlEye
            if battleye_protected:
                if battleye_date == "release":
                    battleye_color = "green"
                else:
                    battleye_color = "orange"
                battleye_text = "Yes"
            else:
                battleye_color = "red"
                battleye_text = "No"
            self.battleye_text.config(text=battleye_text)
            self.draw_circle(self.battleye_canvas, battleye_color)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar informações do servidor: {e}")
            self.status_text.config(text="Erro")
            self.draw_circle(self.status_canvas, "red")
            self.players_online_text.config(text="")
            self.location_text.config(text="")
            self.pvp_type_text.config(text="")
            self.quest_titles_text.config(text="")
            self.battleye_text.config(text="Erro")
            self.draw_circle(self.battleye_canvas, "red")

    def draw_circle(self, canvas, color):
        canvas.delete("all")  # Limpa qualquer desenho anterior
        canvas.create_oval(2, 2, 8, 8, fill=color)

    def open_highscores(self):
        print("Abrindo Highscores...")

    def load_last_selected_server(self):
        try:
            with open("last_server.json", "r") as f:
                return json.load(f).get("last_server")
        except FileNotFoundError:
            return None

    def save_last_selected_server(self, server_name):
        with open("last_server.json", "w") as f:
            json.dump({"last_server": server_name}, f)

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InfoWorldWindow(root)
    root.mainloop()