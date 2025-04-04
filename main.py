import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import json
import requests
import io
import os
from info_world import InfoWorldWindow
from rb_boss import RbBossWindow
from split_loot import SplitLootWindow
from peixe_fear import PeixeFear
from main_help_window import MainHelpWindow
from utils import load_json_config, save_json_config, requisicao_api
import datetime
import pytz 
from atualizador_utils import verificar_atualizacao, baixar_arquivo, iniciar_atualizador

atualizacao = verificar_atualizacao()
if atualizacao:
    print("🆕 Nova versão disponível:", atualizacao["version"])
    print("Changelog:", atualizacao["changelog"])
    resposta = input("Deseja atualizar agora? (s/n): ")
    if resposta.lower() == "s":
        print("⏬ Baixando nova versão...")
        sucesso = baixar_arquivo(atualizacao["url"], "AppTibia_novo.exe")
        if sucesso:
            print("✅ Download concluído. Atualizando...")
            iniciar_atualizador()
        else:
            print("❌ Erro ao baixar atualização.")


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Apps Tibia")
        self.geometry("380x500")  # Aumentando a altura para a nova seção
        self.protocol("WM_DELETE_WINDOW", self.save_main_config_and_exit)

        self.config_file = "config.json"
        self.main_config = load_json_config(self.config_file, {"main_dark_mode": False, "main_x": (self.winfo_screenwidth() - 380) // 2, "main_y": (self.winfo_screenheight() - 500) // 2})
        self.dark_mode = self.main_config.get("main_dark_mode", False)
        self.geometry(f"+{self.main_config.get('main_x', (self.winfo_screenwidth() - 380) // 2)}+{self.main_config.get('main_y', (self.winfo_screenheight() - 500) // 2)}")
        self.atualizar_estilo()

        # --- Seção superior com imagem e mensagem ---
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=(10, 0), padx=10, fill="x")

        self.rashid_image_label = ctk.CTkLabel(self.top_frame, text="")
        self.rashid_image_label.pack(side="left", padx=(0, 10))
        self.load_rashid_image()

        self.rashid_message_label = ctk.CTkLabel(self.top_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.rashid_message_label.pack(side="left", fill="x", expand=True)
        self.update_rashid_message()
        self.after(60 * 60 * 1000, self.schedule_daily_update) # Agendar verificação diária

        # --- Widget para alternar o Dark Mode ---
        self.appearance_mode_switch = ctk.CTkSwitch(
            master=self,
            text="Dark Mode" if self.dark_mode else "Light Mode",
            command=self.toggle_dark_mode
        )
        self.appearance_mode_switch.pack(pady=10, padx=10, anchor="ne")
        self.appearance_mode_switch.select() if self.dark_mode else self.appearance_mode_switch.deselect()

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

        # Botão de Ajuda
        self.help_button = ctk.CTkButton(self, text="Ajuda", command=self.open_help_window)
        self.help_button.pack(pady=10)

    def schedule_daily_update(self):
        now = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        tomorrow_5am = now.replace(hour=5, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        time_until_update = (tomorrow_5am - now).total_seconds() * 1000
        self.after(int(time_until_update), self.daily_update)

    def daily_update(self):
        self.update_rashid_message()
        self.schedule_daily_update()

    def update_rashid_message(self):
        tz_sao_paulo = pytz.timezone('America/Sao_Paulo')
        now_sao_paulo = datetime.datetime.now(tz_sao_paulo)
        hour = now_sao_paulo.hour
        weekday = now_sao_paulo.weekday()  # 0 = Monday, 6 = Sunday

        if hour < 5:
            # Considera o dia anterior
            weekday = (weekday - 1) % 7

        rashid_locations = [
            "Svargrond", "Liberty Bay", "Port Hope", "Ankrahmun", "Darashia", "Edron", "Carlin"
        ]
        location = rashid_locations[weekday]
        self.rashid_message_label.configure(text=f"Rashid está em: {location}")

    def load_rashid_image(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "img", "rashid.gif")
        try:
            rashid_image = Image.open(image_path)
            if hasattr(rashid_image, 'n_frames') and rashid_image.n_frames > 1:
                # É um GIF animado
                self.animate_gif(self.rashid_image_label, image_path)
            else:
                # É uma imagem estática
                rashid_image = rashid_image.resize((50, 50), Image.LANCZOS)
                rashid_photo = ImageTk.PhotoImage(rashid_image)
                self.rashid_image_label.configure(image=rashid_photo)
                self.rashid_image_label.image = rashid_photo
        except FileNotFoundError as e:
            print(f"Erro ao abrir imagem '{image_path}': {e}")

    def animate_gif(self, label, image_path, frame_index=0, size=(50, 50)):
        try:
            gif = Image.open(image_path)
            if frame_index >= gif.n_frames:
                frame_index = 0
            gif.seek(frame_index)
            frame = gif.convert("RGBA")
            resized_frame = frame.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_frame)
            label.configure(image=photo)
            label.image = photo
            self.after(gif.info.get('duration', 100), self.animate_gif, label, image_path, frame_index + 1, size)
        except FileNotFoundError as e:
            print(f"Erro ao abrir GIF '{image_path}': {e}")
        except Exception as e:
            print(f"Erro ao processar GIF '{image_path}': {e}")

    def open_help_window(self):
        help_window = MainHelpWindow(self)

    def save_main_config(self):
        self.main_config["main_dark_mode"] = self.dark_mode
        self.main_config["main_x"] = self.winfo_x()
        self.main_config["main_y"] = self.winfo_y()
        save_json_config(self.config_file, self.main_config)

    def save_main_config_and_exit(self):
        self.save_main_config()
        self.destroy()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.atualizar_estilo()
        if self.dark_mode:
            self.appearance_mode_switch.configure(text="Dark Mode")
        else:
            self.appearance_mode_switch.configure(text="Light Mode")
        self.save_main_config() # Salvar o estado do Dark Mode

    def atualizar_estilo(self):
        if self.dark_mode:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def add_button(self, text, command, row, column, image_path_before=None, image_path_after=None):
        button_frame = ctk.CTkFrame(self.button_frame)
        button_frame.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        icon_size = (20, 20)

        if image_path_before:
            script_dir = os.path.dirname(__file__)
            image_before_path = os.path.join(script_dir, "img", image_path_before.split('/')[-1])
            try:
                image_before = Image.open(image_before_path)
                if hasattr(image_before, 'n_frames') and image_before.n_frames > 1:
                    # É um GIF animado
                    label_before = ctk.CTkLabel(button_frame, text="")
                    label_before.pack(side=ctk.LEFT)
                    self.animate_gif(label_before, image_before_path, size=icon_size)
                else:
                    # É uma imagem estática
                    image_before = image_before.resize(icon_size, Image.LANCZOS)
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
                if hasattr(image_after, 'n_frames') and image_after.n_frames > 1:
                    # É um GIF animado
                    label_after = ctk.CTkLabel(button_frame, text="")
                    label_after.pack(side=ctk.LEFT)
                    self.animate_gif(label_after, image_after_path, size=icon_size)
                else:
                    # É uma imagem estática
                    image_after = image_after.resize(icon_size, Image.LANCZOS)
                    photo_image_after = ImageTk.PhotoImage(image_after)
                    label_after = ctk.CTkLabel(button_frame, image=photo_image_after, text="")
                    label_after.image = photo_image_after
                    label_after.pack(side=ctk.LEFT)
            except FileNotFoundError as e:
                print(f"Erro ao abrir imagem '{image_after_path}': {e}")

        self.buttons[text] = button

    def load_boosted_info(self):
        self.load_boosted_boss()
        self.load_boosted_creature()

    def load_boosted_boss(self):
        endpoint = "boostablebosses"
        data = requisicao_api(endpoint)
        if data and "boostable_bosses" in data and "boosted" in data["boostable_bosses"]:
            boosted_boss = data["boostable_bosses"]["boosted"]
            name = boosted_boss["name"]
            image_url = boosted_boss["image_url"]
            self.boss_name_label.configure(text=name)
            self.load_boosted_image(image_url, self.boss_image_label)
        else:
            self.boss_name_label.configure(text="Erro ao carregar")
            self.boss_image_label.configure(image="")

    def load_boosted_creature(self):
        endpoint = "creatures"
        data = requisicao_api(endpoint)
        if data and "creatures" in data and "boosted" in data["creatures"]:
            boosted_creature = data["creatures"]["boosted"]
            name = boosted_creature["name"]
            image_url = boosted_creature["image_url"]
            self.creature_name_label.configure(text=name)
            self.load_boosted_image(image_url, self.creature_image_label)
        else:
            self.creature_name_label.configure(text="Erro ao carregar")
            self.creature_image_label.configure(image="")

    def load_boosted_image(self, image_url, label):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            resized_image = image.resize((80, 80), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            label.configure(image=photo)
            label.image = photo
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar imagem: {e}")
            label.configure(image="")
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            label.configure(image="")

    def run_app(self, command):
        venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

        if command == "rb_boss.py":
            rb_boss_window = ctk.CTkToplevel(self)
            app = RbBossWindow(rb_boss_window)
        elif command == "info_world.py":
            info_world_window = ctk.CTkToplevel(self)
            app = InfoWorldWindow(info_world_window)
        elif command == "split_loot.py":
            split_loot_window = ctk.CTkToplevel(self)
            app = SplitLootWindow(split_loot_window)
        elif command == "putre_totem.py":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            putre_totem_path = os.path.join(script_dir, "putre_totem.py")
            subprocess.Popen([venv_python, putre_totem_path])
        elif command == "peixe_fear.py":
            peixe_fear_window = ctk.CTkToplevel(self)
            app = PeixeFear(peixe_fear_window)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(script_dir, command)
            subprocess.Popen([venv_python, app_path])

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

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()