import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import json
import requests
import io
import os
from info_world import InfoWorldWindow
from split_loot import SplitLootWindow

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Apps Tibia")
        self.geometry("380x400")

        # Inicialização do modo escuro
        self.dark_mode = False
        self.atualizar_estilo()

        # --- Widget para alternar o Dark Mode ---
        self.appearance_mode_switch = ctk.CTkSwitch(
            master=self,
            text="Dark Mode",
            command=self.toggle_dark_mode
        )
        self.appearance_mode_switch.pack(pady=10, padx=10, anchor="ne")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.buttons = {}

        self.add_button("Boss RB", "rb_boss.py", 0, 0, image_path_before="img/Bakragore.gif")
        self.add_button("ebb flow *Fear*", "peixe_fear.py", 0, 1, image_path_before="img/Bony_Sea_Devil.gif")
        self.add_button("Totem Putre", "putre_totem.py", 1, 0, image_path_before="img/Radicular_Totem.gif")
        self.add_button("SSA/Might", "ssa_might.py", 1, 1, image_path_before="img/Might_Ring.gif", image_path_after="img/Stone_Skin_Amulet.gif")
        self.add_button("Info World", "info_world.py", 2, 0, image_path_before="img/World.png")
        self.add_button("SplitLoot", "split_loot.py", 2, 1, image_path_before="img/Gold_Coin.gif", image_path_after="img/Crystal_Coin.gif")

        # Frame para Boosted Boss e Criatura
        self.boosted_frame = ctk.CTkFrame(self)
        self.boosted_frame.pack(padx=10, pady=10, fill="x")

        # Frame para Boosted Creature (lado esquerdo)
        self.creature_frame = ctk.CTkFrame(self.boosted_frame)
        self.creature_frame.pack(side="left", padx=(0, 5), fill="both", expand=True)

        self.creature_label = ctk.CTkLabel(self.creature_frame, text="Criatura Boosted:", font=("TkDefaultFont", 10, "bold"))
        self.creature_label.pack()
        self.creature_name_label = ctk.CTkLabel(self.creature_frame, text="")
        self.creature_name_label.pack()
        self.creature_image_label = ctk.CTkLabel(self.creature_frame)
        self.creature_image_label.pack()

        # Frame para Boosted Boss (lado direito)
        self.boss_frame = ctk.CTkFrame(self.boosted_frame)
        self.boss_frame.pack(side="right", padx=(5, 0), fill="both", expand=True)

        self.boss_label = ctk.CTkLabel(self.boss_frame, text="Boss Boosted:", font=ctk.CTkFont(size=10, weight="bold"))
        self.boss_label.pack()
        self.boss_name_label = ctk.CTkLabel(self.boss_frame, text="")
        self.boss_name_label.pack()
        self.boss_image_label = ctk.CTkLabel(self.boss_frame)
        self.boss_image_label.pack()

        self.load_boosted_info()
        self.load_button_settings()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.atualizar_estilo()
        if self.dark_mode:
            self.appearance_mode_switch.configure(text="Dark Mode")
        else:
            self.appearance_mode_switch.configure(text="Light Mode")

    def atualizar_estilo(self):
        if self.dark_mode:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def add_button(self, text, command, row, column, image_path_before=None, image_path_after=None):
        button_frame = ctk.CTkFrame(self.button_frame)
        button_frame.grid(row=row, column=column, padx=5, pady=5, sticky="ew")

        if image_path_before:
            script_dir = os.path.dirname(__file__)
            image_before_path = os.path.join(script_dir, "img", image_path_before.split('/')[-1])
            try:
                image_before = Image.open(image_before_path)
                image_before = image_before.resize((20, 20), Image.LANCZOS)
                photo_image_before = ImageTk.PhotoImage(image_before)
                label_before = ctk.CTkLabel(button_frame, image=photo_image_before, text="")
                label_before.image = photo_image_before
                label_before.pack(side=ctk.LEFT)
            except FileNotFoundError as e:
                print(f"Erro ao abrir imagem '{image_before_path}': {e}")

        button = ctk.CTkButton(button_frame, text=text, command=lambda: self.run_app(command))
        button.pack(side=ctk.LEFT)

        if image_path_after:
            script_dir = os.path.dirname(__file__)
            image_after_path = os.path.join(script_dir, "img", image_path_after.split('/')[-1])
            try:
                image_after = Image.open(image_after_path)
                image_after = image_after.resize((20, 20), Image.LANCZOS)
                photo_image_after = ImageTk.PhotoImage(image_after)
                label_after = ctk.CTkLabel(button_frame, image=photo_image_after, text="")
                label_after.image = photo_image_after
                label_after.pack(side=ctk.LEFT)
            except FileNotFoundError as e:
                print(f"Erro ao abrir imagem '{image_after_path}': {e}")

        self.buttons[text] = button

    def run_app(self, command):
        if command == "info_world.py":
            info_world_window = ctk.CTkToplevel(self)
            app = InfoWorldWindow(info_world_window)
        elif command == "split_loot.py":
            split_loot_window = ctk.CTkToplevel(self)
            app = SplitLootWindow(split_loot_window)
        else:
            subprocess.Popen(["python", command])

    def load_button_settings(self):
        try:
            with open("button_settings.json", "r") as f:
                settings = json.load(f)
                for button_name, position in settings.items():
                    if button_name in self.buttons:
                        button = self.buttons[button_name]
                        grid_info = button.grid_info()
                        if grid_info["row"] != position["row"] or grid_info["column"] != position["column"]:
                            button.grid_forget()
                            button.grid(row=position["row"], column=position["column"], padx=5, pady=5, sticky="ew")
        except FileNotFoundError:
            pass

    def load_boosted_info(self):
        self.load_boosted_boss()
        self.load_boosted_creature()

    def load_boosted_boss(self):
        url = "https://api.tibiadata.com/v4/boostablebosses"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data and "boostable_bosses" in data and "boosted" in data["boostable_bosses"]:
                boosted_boss = data["boostable_bosses"]["boosted"]
                name = boosted_boss["name"]
                image_url = boosted_boss["image_url"]
                print(f"Tentando baixar imagem do Boss: {image_url}")
                self.boss_name_label.configure(text=name)
                self.load_image(image_url, self.boss_image_label)
            else:
                self.boss_name_label.configure(text="Erro ao carregar")
                self.boss_image_label.configure(image="")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar boosted boss: {e}")
            self.boss_name_label.configure(text="Erro ao carregar")
            self.boss_image_label.configure(image="")

    def load_boosted_creature(self):
        url = "https://api.tibiadata.com/v4/creatures"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data and "creatures" in data and "boosted" in data["creatures"]:
                boosted_creature = data["creatures"]["boosted"]
                name = boosted_creature["name"]
                image_url = boosted_creature["image_url"]
                print(f"Tentando baixar imagem da Criatura: {image_url}")
                self.creature_name_label.configure(text=name)
                self.load_image(image_url, self.creature_image_label)
            else:
                self.creature_name_label.configure(text="Erro ao carregar")
                self.creature_image_label.configure(image="")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar boosted creature: {e}")
            self.creature_name_label.configure(text="Erro ao carregar")
            self.creature_image_label.configure(image="")

    def load_image(self, image_url, label):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((80, 80), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label.configure(image=photo)
            label.image = photo
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar imagem: {e}")
            label.configure(image="")
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            label.configure(image="")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()