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
        self.show_help_on_startup = True  # Inicialmente mostrar a ajuda

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

        if self.show_help_on_startup:
            self.show_help()

    def show_help(self):
        help_window = HelpWindow(self)

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
                    x = config.get("x", self.default_x)
                    y = config.get("y", self.default_y)
                    self.opacity = config.get("opacity", self.default_opacity)
                    self.show_help_on_startup = config.get("show_help", True)
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
        self.show_help_on_startup = True

    def save_config(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        config = {"x": x, "y": y, "opacity": self.opacity, "show_help": self.show_help_on_startup}
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f)
        except IOError as e:
            print(f"Erro ao salvar a configuração: {e}")

    def save_config_and_exit(self):
        self.save_config()
        self.exit_app()

class HelpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent.root)
        self.title("Putre Totem - Ajuda")
        self.geometry("300x200+300+300")
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        ctk.CTkLabel(self, text="Hotkeys:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        ctk.CTkLabel(self, text="Iniciar/Parar Ciclo: +").pack()
        ctk.CTkLabel(self, text="Fechar App: Ctrl+Shift+Alt+Enter").pack()
        ctk.CTkLabel(self, text="Aumentar Opacidade: Alt + (+)").pack()
        ctk.CTkLabel(self, text="Diminuir Opacidade: Alt + (-)").pack()

        self.show_on_startup_var = tk.BooleanVar(value=self.parent.show_help_on_startup)
        checkbox = ctk.CTkCheckBox(self, text="Não mostrar esta tela novamente", variable=self.show_on_startup_var)
        checkbox.pack(pady=10)

        close_button = ctk.CTkButton(self, text="Fechar", command=self.close_window)
        close_button.pack(pady=5)

    def close_window(self):
        self.parent.show_help_on_startup = not self.show_on_startup_var.get() # Inverte o valor para salvar "não mostrar"
        self.parent.save_config()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    toplevel = tk.Toplevel(root)
    app = PutreTotem(toplevel)
    toplevel.attributes('-topmost', True)
    toplevel.overrideredirect(True)
    toplevel.wm_attributes("-transparentcolor", "white")
    root.mainloop()
