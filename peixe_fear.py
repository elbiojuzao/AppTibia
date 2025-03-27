import tkinter as tk
import winsound
from utils import save_settings, load_settings, apply_settings

class PeixeFear:
    def __init__(self, root):
        self.root = root
        self.root.title("Peixe Fear")
        self.root.overrideredirect(True)
        self.root.geometry("200x100")
        self.root.attributes('-alpha', 0.75)
        self.root.attributes('-topmost', True)

        self.initial_time = 120
        self.time_left = self.initial_time
        self.running = True

        self.timer_label = tk.Label(root, text="2:00", font=("Helvetica", 48))
        self.timer_label.pack(expand=True)

        self.update_timer()
        self.create_menu()

        self.moving = False
        self.resizing = False
        self.x, self.y = 0, 0
        self.original_width = self.root.winfo_width()
        self.original_height = self.root.winfo_height()

        self.root.bind("<Button-3>", self.show_menu)

        self.beep_type = "long"
        apply_settings(self.root, "peixe_fear")

    def update_timer(self):
        if self.running:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            time_string = f"{minutes}:{seconds:02d}"
            self.timer_label.config(text=time_string)

            if self.time_left <= 10:
                color = self.get_color()
                self.timer_label.config(fg=color)

            if self.time_left > 0:
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.time_left = self.initial_time
                self.timer_label.config(text="2:00", fg="black")
                self.play_beep()
                self.update_timer()

    def get_color(self):
        if self.time_left <= 5:
            red = 255
            green = int(255 * (self.time_left / 5))
            blue = 0
        else:
            red = 255
            green = 165
            blue = 0
        return f"#{red:02x}{green:02x}{blue:02x}"

    def create_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)

        self.actions_menu = tk.Menu(self.menu, tearoff=0)
        self.actions_menu.add_command(label="Iniciar", command=self.start_timer)
        self.actions_menu.add_command(label="Pausar", command=self.pause_timer)
        self.actions_menu.add_command(label="Reiniciar", command=self.restart_timer)
        self.actions_menu.add_separator()
        self.actions_menu.add_command(label="Bip Longo", command=lambda: self.set_beep_type("long"))
        self.actions_menu.add_command(label="Bip Curto", command=lambda: self.set_beep_type("short"))
        self.menu.add_cascade(label="Ações", menu=self.actions_menu)

        self.opacity_menu = tk.Menu(self.menu, tearoff=0)
        self.opacity_menu.add_command(label="1.0", command=lambda: self.update_opacity(1.0))
        self.opacity_menu.add_command(label="0.75", command=lambda: self.update_opacity(0.75))
        self.opacity_menu.add_command(label="0.5", command=lambda: self.update_opacity(0.5))
        self.opacity_menu.add_command(label="0.25", command=lambda: self.update_opacity(0.25))
        self.opacity_menu.add_command(label="0.10", command=lambda: self.update_opacity(0.10))
        self.menu.add_cascade(label="Opacidade", menu=self.opacity_menu)

        self.menu.add_command(label="Mover", command=self.start_move)
        self.menu.add_command(label="Redimensionar", command=self.start_resize)
        self.menu.add_command(label="Fechar", command=self.close)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def pause_timer(self):
        self.running = False

    def restart_timer(self):
        self.running = False
        self.time_left = self.initial_time
        self.timer_label.config(text="2:00", fg="black")
        self.running = True
        self.update_timer()

    def update_opacity(self, value):
        self.root.attributes('-alpha', value)

    def start_move(self):
        self.moving = True
        self.root.bind("<B1-Motion>", self.move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)

    def move(self, event):
        if self.moving:
            self.root.geometry(f"+{event.x_root}+{event.y_root}")

    def stop_move(self, event):
        self.moving = False
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonRelease-1>")

    def start_resize(self):
        self.resizing = True
        self.root.bind("<B1-Motion>", self.resize_proportional)
        self.root.bind("<ButtonRelease-1>", self.stop_resize)

    def resize_proportional(self, event):
        if self.resizing:
            width_ratio = event.x / self.original_width
            height_ratio = event.y / self.original_height
            ratio = max(width_ratio, height_ratio)
            new_width = int(self.original_width * ratio)
            new_height = int(self.original_height * ratio)
            self.root.geometry(f"{new_width}x{new_height}")

    def stop_resize(self, event):
        self.resizing = False
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonRelease-1>")

    def close(self):
        save_settings(self.root, "peixe_fear")
        self.root.destroy()

    def set_beep_type(self, beep_type):
        self.beep_type = beep_type

    def play_beep(self):
        frequency = 2500
        duration = 200 if self.beep_type == "long" else 150
        winsound.Beep(frequency, duration)
        winsound.Beep(frequency, duration)

if __name__ == "__main__":
    root = tk.Tk()
    app = PeixeFear(root)
    root.mainloop()