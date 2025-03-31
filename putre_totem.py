import tkinter as tk
import customtkinter as ctk
import json
import os

class PutreTotem:
    def __init__(self, root):
        self.root = root
        self.root.title("Direction Indicator")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")

        self.config_file = "config.json"

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

        self.default_x = 100
        self.default_y = 100
        self.default_opacity = 0.8
        self.load_config()

        self.root.bind("<+>", self.start_direction_cycle)
        self.root.bind("<Control-Shift-Alt-Return>", self.exit_app)
        self.root.bind("<Alt-plus>", self.increase_opacity)
        self.root.bind("<Alt-minus>", self.decrease_opacity)

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
            self.root.after(1000, self.update_timer_seconds)

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

    def update_timer_seconds(self):
        if self.is_active:
            self.update_osd_text()
            self.root.after(1000, self.update_timer_seconds)

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

    def increase_opacity(self, event):
        current_opacity = self.root.attributes('-alpha')
        new_opacity = min(1.0, current_opacity + 0.05)
        self.root.attributes('-alpha', new_opacity)
        self.opacity = new_opacity

    def decrease_opacity(self, event):
        current_opacity = self.root.attributes('-alpha')
        new_opacity = max(0.1, current_opacity - 0.05)
        self.root.attributes('-alpha', new_opacity)
        self.opacity = new_opacity

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    x = config.get("putre_totem_x", self.default_x)
                    y = config.get("putre_totem_y", self.default_y)
                    self.opacity = config.get("putre_totem_opacity", self.default_opacity)
                    self.root.geometry(f"+{x}+{y}")
                    self.root.attributes('-alpha', self.opacity)
            except (FileNotFoundError, json.JSONDecodeError):
                self.load_default_config()
        else:
            self.load_default_config()

    def load_default_config(self):
        self.root.geometry(f"+{self.default_x}+{self.default_y}")
        self.root.attributes('-alpha', self.default_opacity)
        self.opacity = self.default_opacity

    def save_config(self):
        try:
            with open(self.config_file, "r+") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    config = {}
                config["putre_totem_x"] = self.root.winfo_x()
                config["putre_totem_y"] = self.root.winfo_y()
                config["putre_totem_opacity"] = self.opacity
                f.seek(0)
                json.dump(config, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            config = {
                "putre_totem_x": self.root.winfo_x(),
                "putre_totem_y": self.root.winfo_y(),
                "putre_totem_opacity": self.opacity
            }
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar a configuração: {e}")

    def save_config_and_exit(self):
        self.save_config()
        self.exit_app()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    toplevel = tk.Toplevel(root)
    app = PutreTotem(toplevel)
    toplevel.attributes('-topmost', True)
    toplevel.overrideredirect(True)
    toplevel.wm_attributes("-transparentcolor", "white")
    root.mainloop()