import tkinter as tk
import time
import json
import os
from tkinter import colorchooser
from utils import save_settings, load_settings

class DirectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Totem Putre")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.resizable(False, False)

        self.load_settings()

        self.root.attributes('-alpha', 0.75)

        self.original_counter_font_size = 60
        self.original_direction_font_size = 80

        self.counter_label = tk.Label(root, text="", font=("Helvetica", self.original_counter_font_size), anchor=tk.CENTER)
        self.counter_label.grid(row=0, column=0, sticky="nsew")

        self.direction_label = tk.Label(root, text="", font=("Helvetica", self.original_direction_font_size), anchor=tk.CENTER)
        self.direction_label.grid(row=0, column=1, padx=2, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.running = False
        self.counter = 5
        self.directions = ["↥", "↦", "↧", "↤"]
        self.current_direction = 0

        self.menu = tk.Menu(root, tearoff=0)
        self.actions_menu = tk.Menu(self.menu, tearoff=0)
        self.opacity_menu = tk.Menu(self.menu, tearoff=0)

        self.actions_menu.add_command(label="Iniciar", command=self.start)
        self.actions_menu.add_command(label="Pausar", command=self.pause)
        self.actions_menu.add_command(label="Reiniciar", command=self.restart)
        self.actions_menu.add_command(label="Mudar Cor da Fonte", command=self.change_font_color)

        self.opacity_menu.add_command(label="1.0", command=lambda: self.update_opacity(1.0))
        self.opacity_menu.add_command(label="0.75", command=lambda: self.update_opacity(0.75))
        self.opacity_menu.add_command(label="0.5", command=lambda: self.update_opacity(0.5))
        self.opacity_menu.add_command(label="0.25", command=lambda: self.update_opacity(0.25))
        self.opacity_menu.add_command(label="0.10", command=lambda: self.update_opacity(0.10))

        self.menu.add_cascade(label="Ações", menu=self.actions_menu)
        self.menu.add_cascade(label="Opacidade", menu=self.opacity_menu)
        self.menu.add_command(label="Mover", command=self.start_move)
        self.menu.add_command(label="Redimensionar", command=self.start_resize)
        self.menu.add_command(label="Fechar", command=self.close)

        self.root.bind("<Button-3>", self.show_menu)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.moving = False
        self.resizing = False
        self.x, self.y = 0, 0
        self.original_width = self.root.winfo_width()
        self.original_height = self.root.winfo_height()

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def start(self):
        if not self.running:
            self.running = True
            self.root.wm_attributes('-transparentcolor', 'white')
            self.update_direction()

    def pause(self):
        self.running = False

    def restart(self):
        self.running = False
        self.counter = 5
        self.direction_label.config(text="")
        self.counter_label.config(text="")
        self.current_direction = 0

    def update_direction(self):
        if self.running:
            direction = self.directions[self.current_direction]
            font_size = self.original_direction_font_size
            self.direction_label.config(text=direction, font=("Helvetica", font_size))
            self.counter = 5
            self.update_counter()

    def update_counter(self):
        if self.running:
            self.counter_label.config(text=str(self.counter))
            if self.counter > 0:
                self.counter -= 1
                self.root.after(1000, self.update_counter)
            else:
                self.current_direction = (self.current_direction + 1) % 4
                self.update_direction()

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

    def start_resize(self, event):
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

            new_counter_font_size = int(self.original_counter_font_size * ratio)
            new_direction_font_size = int(self.original_direction_font_size * ratio)
            self.counter_label.config(font=("Helvetica", new_counter_font_size))
            self.direction_label.config(font=("Helvetica", new_direction_font_size))

    def stop_resize(self, event):
        self.resizing = False
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonRelease-1>")

    def change_font_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.counter_label.config(fg=color)
            self.direction_label.config(fg=color)

    def close(self):
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectionApp(root)
    root.mainloop()