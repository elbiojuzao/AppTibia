import tkinter as tk
import customtkinter as ctk
import winsound
from utils import save_json_config, load_json_config

CONFIG_KEY_PUTRE_TOTEM = "putre_totem_settings"
CONFIG_FILE = "config.json"

class PutreTotemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Direction Indicator")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.configure(bg="white")
        self.app_name = "putre_totem"
        self.opacity = self.root.attributes('-alpha') # Inicializa a opacidade

        self.app_name = "putre_totem"
        self.total_time = 5 
        self.counter = self.total_time
        self.is_active = True  
        self.is_running = False 
        self.direction = 0

        self.font = ctk.CTkFont(size=48)
        self.label_width = 200
        self.label_height = 80
        self.text_label = ctk.CTkLabel(self.root, text="2:00", font=self.font, text_color="lime",
                                            bg_color="white", fg_color="white", 
                                            width=self.label_width, height=self.label_height)
        self.text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Inicia o timer automaticamente na criação
        self.root.after(100, self.start_timer_initial) 

        self.root.bind("<+>", self.start_direction_cycle)
        self.root.bind("<Control-Shift-Alt-Return>", self.exit_app)
        self.root.bind("<Alt-plus>", self.increase_opacity)
        self.root.bind("<Alt-minus>", self.decrease_opacity)
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)

        self.x_offset = 0
        self.y_offset = 0

        self.root.protocol("WM_DELETE_WINDOW", self.save_config_and_exit)

    def load_config(self):
        config = load_json_config(CONFIG_FILE, {})
        putre_totem_settings = config.get(CONFIG_KEY_PUTRE_TOTEM, {
            "geometry": f"200x100+{self.root.winfo_screenwidth()//2 - 100}+{self.root.winfo_screenheight()//2 - 50}",
            "alpha": 0.8
        })
        self.root.geometry(putre_totem_settings.get("geometry"))
        self.root.attributes('-alpha', putre_totem_settings.get("alpha"))
        self.opacity = self.root.attributes('-alpha')

    def save_config(self):
        config = load_json_config(CONFIG_FILE, {})
        settings = {"geometry": self.root.geometry(), "alpha": self.root.attributes('-alpha')}
        config[CONFIG_KEY_PUTRE_TOTEM] = settings
        save_json_config(CONFIG_FILE, config)

    def start_timer_initial(self):
        if self.is_active and not self.is_running:
            self.is_running = True
            self.update_timer()

    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def on_drag(self, event):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f"+{x}+{y}")

    def start_direction_cycle(self, event=None):
        self.is_active = True
        self.counter = self.total_time
        if not self.is_active:
            self.is_active = True
            self.counter = 0
            self.direction = 0
            self.update_osd_text()
            self.root.after(1000, self.update_timer)

    def update_timer(self):
        if self.is_active:
            if self.total_time - self.counter > 0:
                self.update_osd_text()
                self.root.after(1000, self.update_timer)
                self.counter += 1
            else:
                self.direction = (self.direction + 1) % 4
                self.counter = 0
                self.update_osd_text()
                self.root.after(10, self.update_timer)

    def update_osd_text(self):
        time_display = self.total_time - self.counter
        sec = max(0, time_display)

        if self.direction == 0:
            direction_char = "N↑"
        elif self.direction == 1:
            direction_char = "D→"
        elif self.direction == 2:
            direction_char = "S↓"
        elif self.direction == 3:
            direction_char = "E←"
        else:
            direction_char = "?"

        self.text_label.configure(text=f"{direction_char}{sec}")

    def increase_opacity(self, event):
        current_opacity = self.root.attributes('-alpha')
        new_opacity = min(1.0, current_opacity + 0.05)
        self.root.attributes('-alpha', new_opacity)
        
    def decrease_opacity(self, event):
        current_opacity = self.root.attributes('-alpha')
        new_opacity = max(0.1, current_opacity - 0.05)
        self.root.attributes('-alpha', new_opacity)

    def play_beep(self):
        for _ in range(2):
            winsound.Beep(1000, 300)

    def exit_app(self, event=None):
        self.is_active = False
        self.root.destroy()

    def save_config_and_exit(self):
        self.save_settings()
        self.exit_app()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    toplevel = ctk.CTkToplevel(root)
    app = PutreTotemApp(toplevel)
    root.mainloop()