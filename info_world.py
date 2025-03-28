import customtkinter as ctk
import requests
import json

class InfoWorldWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Informações do Mundo")
        self.geometry("400x450") # Ajustei a altura para acomodar o botão

        # Carrega o último servidor selecionado
        self.last_selected_server = self.load_last_selected_server()

        # Dropdown com nomes de servidores
        self.servers = self.fetch_server_names()
        self.server_var = ctk.StringVar(self)
        if self.last_selected_server and self.last_selected_server in self.servers:
            self.server_var.set(self.last_selected_server)
        else:
            self.server_var.set("Antica")
        self.server_dropdown = ctk.CTkComboBox(self, variable=self.server_var, values=self.servers, state="readonly")
        self.server_dropdown.pack(pady=10, padx=10)
        # self.server_dropdown.bind("<<ComboboxSelected>>", self.update_world_info)
        self.server_var.trace_add("write", self.on_server_change)

        # Frame para status com bolinha
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(pady=2, padx=10, fill="x")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Status:", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(side=ctk.LEFT)
        self.status_canvas = ctk.CTkCanvas(self.status_frame, width=10, height=10, highlightthickness=0)
        self.status_canvas.pack(side=ctk.LEFT, padx=5)
        self.status_text = ctk.CTkLabel(self.status_frame, text="")
        self.status_text.pack(side=ctk.LEFT)

        # Frame para players online
        self.players_online_frame = ctk.CTkFrame(self)
        self.players_online_frame.pack(pady=2, padx=10, fill="x")
        self.players_online_label = ctk.CTkLabel(self.players_online_frame, text="Players Online:", font=ctk.CTkFont(weight="bold"))
        self.players_online_label.pack(side=ctk.LEFT)
        self.players_online_text = ctk.CTkLabel(self.players_online_frame, text="")
        self.players_online_text.pack(side=ctk.LEFT)

        # Frame para localização
        self.location_frame = ctk.CTkFrame(self)
        self.location_frame.pack(pady=2, padx=10, fill="x")
        self.location_label = ctk.CTkLabel(self.location_frame, text="Location:", font=ctk.CTkFont(weight="bold"))
        self.location_label.pack(side=ctk.LEFT)
        self.location_text = ctk.CTkLabel(self.location_frame, text="")
        self.location_text.pack(side=ctk.LEFT)

        # Frame para tipo de PVP
        self.pvp_type_frame = ctk.CTkFrame(self)
        self.pvp_type_frame.pack(pady=2, padx=10, fill="x")
        self.pvp_type_label = ctk.CTkLabel(self.pvp_type_frame, text="PVP Type:", font=ctk.CTkFont(weight="bold"))
        self.pvp_type_label.pack(side=ctk.LEFT)
        self.pvp_type_text = ctk.CTkLabel(self.pvp_type_frame, text="")
        self.pvp_type_text.pack(side=ctk.LEFT)

        # Frame para títulos de quests
        self.quest_titles_label = ctk.CTkLabel(self, text="Quest Titles:", justify="left", anchor="nw", font=ctk.CTkFont(weight="bold"))
        self.quest_titles_label.pack(padx=10, pady=(10, 2), fill="x")
        self.quest_titles_text = ctk.CTkLabel(self, text="", justify="left", anchor="nw")
        self.quest_titles_text.pack(padx=10, fill="x")

        # Frame para BattlEye com bolinha
        self.battleye_frame = ctk.CTkFrame(self)
        self.battleye_frame.pack(pady=2, padx=10, fill="x")
        self.battleye_label = ctk.CTkLabel(self.battleye_frame, text="BattlEye Protected:", font=ctk.CTkFont(weight="bold"))
        self.battleye_label.pack(side=ctk.LEFT)
        self.battleye_canvas = ctk.CTkCanvas(self.battleye_frame, width=10, height=10, highlightthickness=0)
        self.battleye_canvas.pack(side=ctk.LEFT, padx=5)
        self.battleye_text = ctk.CTkLabel(self.battleye_frame, text="")
        self.battleye_text.pack(side=ctk.LEFT)

        # Botões "Highscores"
        self.highscores_button = ctk.CTkButton(self, text="Highscores", command=self.open_highscores)
        self.highscores_button.pack(pady=10, padx=10)

        self.update_world_info(None)  # Carrega informações do primeiro servidor ao iniciar

        # Salva o último servidor selecionado ao fechar a janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_server_change(self, *args):
        self.update_world_info(None)

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
            self.status_text.configure(text=status)
            self.draw_circle(self.status_canvas, "green" if status == "online" else "red")

            players_online = world['players_online']
            self.players_online_text.configure(text=f"{players_online}")
            location = world['location']
            self.location_text.configure(text=f"{location}")
            pvp_type = world['pvp_type']
            self.pvp_type_text.configure(text=f"{pvp_type}")

            # Formata os títulos de quests
            quest_titles = world['world_quest_titles']
            if quest_titles:
                formatted_titles = "\n".join([f"  - {title}" for title in quest_titles])
            else:
                formatted_titles = "None"
            self.quest_titles_text.configure(text=f"{formatted_titles}")

            # Atualiza o BattlEye com a bolinha
            battleye_protected = world['battleye_protected']
            battleye_date = world.get('battleye_date')  # Obtém a data do BattlEye
            if battleye_protected:
                if battleye_date == "release":
                    battleye_color = "green"
                else:
                    battleye_color = "orange"
                battleye_text = "Yes"
            else:
                battleye_color = "red"
                battleye_text = "No"
            self.battleye_text.configure(text=battleye_text)
            self.draw_circle(self.battleye_canvas, battleye_color)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar informações do servidor: {e}")
            self.status_text.configure(text="Erro")
            self.draw_circle(self.status_canvas, "red")
            self.players_online_text.configure(text="")
            self.location_text.configure(text="")
            self.pvp_type_text.configure(text="")
            self.quest_titles_text.configure(text="")
            self.battleye_text.configure(text="Erro")
            self.draw_circle(self.battleye_canvas, "red")
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

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
        self.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = InfoWorldWindow(root)
    root.mainloop()