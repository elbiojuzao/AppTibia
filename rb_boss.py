import tkinter as tk
import json
import os
import time

class RBBoss:
    def __init__(self, root):
        self.root = root
        self.root.title("RB Boss")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.initial_time = 90  # 1 minuto e 30 segundos
        self.time_left = self.initial_time
        self.running = False

        self.punish_label = tk.Label(root, text="", font=("Helvetica", 24), fg="red")
        self.punish_label.pack()

        self.timer_label = tk.Label(root, text="1:30", font=("Helvetica", 24))
        self.timer_label.pack()

        # Define o tamanho fixo da tela
        self.root.geometry("200x100") # Ajuste os valores conforme necessário

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Iniciar", command=self.start_timer)
        self.menu.add_command(label="Pausar", command=self.pause_timer)
        self.menu.add_command(label="Mover", command=self.start_move)
        self.menu.add_command(label="Fechar", command=self.close)

        self.root.bind("<Button-3>", self.show_menu)

        self.first_run = True  # Variável de controle
        self.load_settings()

        self.moving = False  # Variável de controle para o movimento

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def pause_timer(self):
        self.running = False

    def update_timer(self):
        if self.running:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            time_string = f"{minutes}:{seconds:02d}"
            self.timer_label.config(text=time_string)

            if not self.first_run:  # Verifica se não é a primeira execução
                if self.time_left == 84:
                    self.punish_label.config(text="PUNISH")
                elif self.time_left == 78:
                    self.punish_label.config(text="RAAAR")
                    self.blink_raaar(2)
                elif self.time_left == 76:
                    self.punish_label.config(text="Blood Jaw", fg="red")

            if self.time_left == 10:
                self.punish_label.config(text="Atenção", fg="yellow")
            elif self.time_left == 5:
                self.punish_label.config(text="Sobe", fg="red")

            if self.time_left > 0:
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.time_left = self.initial_time  # Reinicia o contador
                self.punish_label.config(text="") # Limpa a label
                self.first_run = False  # Indica que não é mais a primeira execução
                self.update_timer()

    def blink_raaar(self, count):
        if count > 0:
            current_color = self.punish_label.cget("fg")
            new_color = "yellow" if current_color == "red" else "red"
            self.punish_label.config(fg=new_color)
            self.root.after(500, lambda: self.blink_raaar(count - 1))

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

    def close(self):
        self.save_settings()
        self.root.destroy()

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                settings = json.load(f)
                if "position" in settings:
                    self.root.geometry(settings["position"])
                if "opacity" in settings:
                    self.root.attributes('-alpha', settings["opacity"])
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            "position": "+{}+{}".format(self.root.winfo_x(), self.root.winfo_y()),
            "opacity": self.root.attributes('-alpha')
        }
        with open("config.json", "w") as f:
            json.dump(settings, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = RBBoss(root)
    root.mainloop()