import tkinter as tk
import customtkinter as ctk
import winsound
from utils import save_json_config, load_json_config, increase_opacity, decrease_opacity

CONFIG_KEY_PEIXE_FEAR = "peixe_fear_settings"
CONFIG_FILE = "config.json"

class PeixeFear:
    def __init__(self, root):
        self.root = root
        self.root.title("Peixe Fear")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.configure(bg="white")  

        self.app_name = "peixe_fear"
        self.total_time = 120  # 2 minutos
        self.counter = self.total_time
        self.is_active = True  
        self.is_running = False 

        self.font = ctk.CTkFont(size=48)
        self.label_width = 200
        self.label_height = 80
        self.text_label = ctk.CTkLabel(self.root, text="2:00", font=self.font, text_color="lime",
                                            bg_color="white", fg_color="white",  # Remove bordas cinzas
                                            width=self.label_width, height=self.label_height)
        self.text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.load_settings()

        # Inicia o timer automaticamente na criação
        self.root.after(100, self.start_timer_initial) 

        self.root.bind("<plus>", self.start_or_restart_timer)
        self.root.bind("<Control-Shift-Alt-Return>", self.exit_app)
        self.root.bind("<Alt-plus>", self.increase_opacity)
        self.root.bind("<Alt-minus>", self.decrease_opacity)

        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.x_offset = 0
        self.y_offset = 0

        self.root.protocol("WM_DELETE_WINDOW", self.save_config_and_exit)

    def load_settings(self):
        config = load_json_config(CONFIG_FILE, {})
        peixe_fear_settings = config.get(CONFIG_KEY_PEIXE_FEAR, {"geometry": f"200x100+{self.root.winfo_screenwidth()//2 - 100}+{self.root.winfo_screenheight()//2 - 50}", "alpha": 0.75})
        self.root.geometry(peixe_fear_settings.get("geometry"))
        self.root.attributes('-alpha', peixe_fear_settings.get("alpha"))

    def save_settings(self):
        config = load_json_config(CONFIG_FILE, {})
        settings = {"geometry": self.root.geometry(), "alpha": self.root.attributes('-alpha')}
        config[CONFIG_KEY_PEIXE_FEAR] = settings
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

    def start_or_restart_timer(self, event=None):
        self.is_active = True
        self.counter = self.total_time
        if not self.is_running:
            self.is_running = True
            self.update_timer()

    def update_timer(self):
        if self.is_active and self.is_running:
            if self.counter > 0:
                minutes = self.counter // 60
                seconds = self.counter % 60
                self.text_label.configure(text=f"{minutes}:{seconds:02}")
                self.counter -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.play_beep()
                self.counter = self.total_time  # Reinicia o contador
                self.text_label.configure(text="2:00") 
                self.root.after(10, self.update_timer) 
                # self.is_running permanece True para continuar o loop


    def increase_opacity_event(self, event):
        increase_opacity(self.root)

    def decrease_opacity_event(self, event):
        decrease_opacity(self.root)
        
    def play_beep(self):
        for _ in range(2):
            winsound.Beep(1000, 300)

    def exit_app(self, event=None):
        self.is_active = False
        self.is_running = False
        self.root.destroy()

    def save_config_and_exit(self):
        self.save_settings()
        self.exit_app()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    toplevel = ctk.CTkToplevel(root)
    app = PeixeFear(toplevel)
    root.mainloop()