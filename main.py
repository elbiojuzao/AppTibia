import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import json
import os

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Aplicativos")

        self.button_frame = ttk.Frame(root, padding=10)
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        self.buttons = {}

        self.add_button("RB Boss", "rb_boss.py", 0, 0)
        self.add_button("Peixe Fear", "peixe_fear.py", 0, 1)
        self.add_button("Totem Putre", "putre_totem.py", 1, 0)
        self.add_button("SSA Might", "ssa_might.py", 1, 1, image_path_before="img/Might_Ring.gif", image_path_after="img/Stone_Skin_Amulet.gif")

        self.load_button_settings()

    def add_button(self, text, command, row, column, image_path_before=None, image_path_after=None):
        button_frame = ttk.Frame(self.button_frame)
        button_frame.grid(row=row, column=column, padx=5, pady=5, sticky="ew")

        if image_path_before:
            image_before = Image.open(image_path_before)
            image_before = image_before.resize((20, 20), Image.LANCZOS)
            photo_image_before = ImageTk.PhotoImage(image_before)
            label_before = ttk.Label(button_frame, image=photo_image_before)
            label_before.image = photo_image_before
            label_before.pack(side=tk.LEFT)

        button = ttk.Button(button_frame, text=text, command=lambda: self.run_app(command))
        button.pack(side=tk.LEFT)
        if image_path_after:
            image_after = Image.open(image_path_after)
            image_after = image_after.resize((20, 20), Image.LANCZOS)
            photo_image_after = ImageTk.PhotoImage(image_after)
            label_after = ttk.Label(button_frame, image=photo_image_after)
            label_after.image = photo_image_after
            label_after.pack(side=tk.LEFT)

        self.buttons[text] = button

    def run_app(self, command):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()