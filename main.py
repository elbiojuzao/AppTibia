import tkinter as tk
import subprocess

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry("200x150") # Altera o tamanho da tela para 200x150

        self.create_buttons()
        self.create_menu()

        self.moving = False
        self.resizing = False
        self.x, self.y = 0, 0
        self.original_width = self.root.winfo_width()
        self.original_height = self.root.winfo_height()

        self.root.bind("<Button-3>", self.show_menu)

    def create_buttons(self):
        putrefactory_button = tk.Button(self.root, text="Putrefactory", command=self.open_putrefactory)
        putrefactory_button.pack(pady=10)

        peixe_fear_button = tk.Button(self.root, text="Peixe Fear", command=self.open_peixe_fear)
        peixe_fear_button.pack(pady=10)

        rb_boss_button = tk.Button(self.root, text="RB Boss", command=self.open_rb_boss)
        rb_boss_button.pack(pady=10)

    def create_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Mover", command=self.start_move)
        self.menu.add_command(label="Redimensionar", command=self.start_resize)
        self.menu.add_command(label="Fechar", command=self.close)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def open_putrefactory(self):
        subprocess.Popen(["python", "direction_app.py"])
        self.root.destroy()

    def open_peixe_fear(self):
        subprocess.Popen(["python", "peixe_fear.py"])
        self.root.destroy()

    def open_rb_boss(self):
        subprocess.Popen(["python", "rb_boss.py"])
        self.root.destroy()

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
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StartScreen(root)
    root.mainloop()