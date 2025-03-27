import tkinter as tk
import time
import winsound
from utils import save_settings, load_settings, apply_settings

class RBBoss:
    def __init__(self, root):
        self.root = root
        self.root.title("RB Boss")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.initial_time = 90
        self.time_left = self.initial_time
        self.running = False
        self.beep_ligado = False

        self.punish_label = tk.Label(root, text="", font=("Helvetica", 24), fg="red")
        self.punish_label.pack()

        self.timer_label = tk.Label(root, text="1:30", font=("Helvetica", 24))
        self.timer_label.pack()

        self.root.geometry("200x100")

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Iniciar", command=self.start_timer)
        self.menu.add_command(label="Pausar", command=self.pause_timer)
        self.menu.add_command(label="Mover", command=self.start_move)
        self.menu.add_command(label="Beep", command=self.alternar_beep)
        self.menu.add_command(label="Fechar", command=self.close)

        self.root.bind("<Button-3>", self.show_menu)

        self.first_run = True 
        apply_settings(self.root, "rb_boss") 

        self.moving = False

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def pause_timer(self):
        self.running = False

    def alternar_beep(self):
        self.beep_ligado = not self.beep_ligado
        if self.beep_ligado:
            self.menu.entryconfig("Beep", label="Sem Beep")
        else:
            self.menu.entryconfig("Beep", label="Beep")

    def beep(self):
        winsound.Beep(2500, 150)
        winsound.Beep(2500, 150)

    def update_timer(self):
        if self.running:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            time_string = f"{minutes}:{seconds:02d}"
            self.timer_label.config(text=time_string)

            if not self.first_run:
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
                self.time_left = self.initial_time
                self.punish_label.config(text="") 
                self.first_run = False 
                self.update_timer()
                if self.beep_ligado:
                    self.beep()
                    self.beep()

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
        save_settings(self, "rb_boss") 
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RBBoss(root)
    root.mainloop()