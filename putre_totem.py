import tkinter as tk
import customtkinter as ctk
import os
from utils import save_json_config, load_json_config, increase_opacity, decrease_opacity

CONFIG_KEY_PUTRE_TOTEM = "putre_totem_settings"
CONFIG_FILE = "config.json"

class PutreTotem:
    def __init__(self, root):
        self.root = root
        self.root.title("Direction Indicator")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.configure(bg="white")

        self.app_name = "putre_totem"
        self.total_time = 5
        self.counter = 0
        self.direction = 0
        self.is_active = False

        self.font = ctk.CTkFont(size=48)
        self.label_width = 100
        self.label_height = 50
        self.text_label = ctk.CTkLabel(self.root, text="N↑6", font=self.font, text_color="lime",
                                            bg_color='white', fg_color='transparent',
                                            width=self.label_width, height=self.label_height)
        self.text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.load_config()

        self.root.bind("<+>", self.start_direction_cycle)
        self.root.bind("<Control-Shift-Alt-Return>", self.exit_app)
        self.root.bind("<Alt-plus>", self.increase_opacity_event)
        self.root.bind("<Alt-minus>", self.decrease_opacity_event)

        # --- Funcionalidade de arrastar ---
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.x_offset = 0
        self.y_offset = 0

        self.root.protocol("WM_DELETE_WINDOW", self.save_config_and_exit)

    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def on_drag(self, event):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f"+{x}+{y}")

    def start_direction_cycle(self, event=None):
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
                self.root.after(1000, self.update_timer)

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

    def exit_app(self, event=None):
        self.is_active = False
        self.root.destroy()

    def increase_opacity_event(self, event):
        increase_opacity(self.root)

    def decrease_opacity_event(self, event):
        decrease_opacity(self.root)

    def load_config(self):
        config = load_json_config(CONFIG_FILE, {})
        putre_totem_settings = config.get(CONFIG_KEY_PUTRE_TOTEM, {"geometry": f"100x50+{self.root.winfo_screenwidth()//2 - 50}+{self.root.winfo_screenheight()//2 - 25}", "alpha": 0.8})
        self.root.geometry(putre_totem_settings.get("geometry"))
        self.root.attributes('-alpha', putre_totem_settings.get("alpha"))
        self.opacity = self.root.attributes('-alpha')

    def save_config(self):
        config = load_json_config(CONFIG_FILE, {})
        settings = {"geometry": self.root.geometry(), "alpha": self.root.attributes('-alpha')}
        config[CONFIG_KEY_PUTRE_TOTEM] = settings
        save_json_config(CONFIG_FILE, config)

    def save_config_and_exit(self):
        self.save_config()
        self.exit_app()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    toplevel = ctk.CTkToplevel(root)
    app = PutreTotem(toplevel)
    root.mainloop()