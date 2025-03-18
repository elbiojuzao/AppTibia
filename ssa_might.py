import tkinter as tk
from PIL import Image, ImageTk
import mss
import pygetwindow as gw
from utils import save_settings, load_settings

class SSAMight:
    def __init__(self, root):
        self.root = root
        self.root.title("SSA Might")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.capture_area = {"left": 100, "top": 100, "width": 300, "height": 200}
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.moving = False
        self.x, self.y = 0, 0
        self.root.bind("<Button-3>", self.show_menu)

        self.selection_mode = False
        self.selection_start_x = 0
        self.selection_start_y = 0
        self.selection_end_x = 0
        self.selection_end_y = 0
        self.selection_rectangle = None

        self.load_settings()
        self.update_capture()
        self.create_menu()

    def update_capture(self):
        with mss.mss() as sct:
            sct_img = sct.grab(self.capture_area)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
            self.root.after(100, self.update_capture)

    def create_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)
        self.opacity_menu = tk.Menu(self.menu, tearoff=0)
        self.opacity_menu.add_command(label="1.0", command=lambda: self.update_opacity(1.0))
        self.opacity_menu.add_command(label="0.75", command=lambda: self.update_opacity(0.75))
        self.opacity_menu.add_command(label="0.5", command=lambda: self.update_opacity(0.5))
        self.opacity_menu.add_command(label="0.25", command=lambda: self.update_opacity(0.25))
        self.opacity_menu.add_command(label="0.10", command=lambda: self.update_opacity(0.10))
        self.menu.add_cascade(label="Opacidade", menu=self.opacity_menu)
        self.menu.add_command(label="Mover", command=self.start_move)
        self.menu.add_cascade(label="Transmitir", menu=self.create_transmit_menu())
        self.menu.add_command(label="Window", command=self.start_selection)
        self.menu.add_command(label="Fechar", command=self.close)

    def create_transmit_menu(self):
        transmit_menu = tk.Menu(self.menu, tearoff=0)
        windows = gw.getAllTitles()
        for window in windows:
            if window:
                transmit_menu.add_command(label=window, command=lambda w=window: self.transmit_to(w))
        return transmit_menu

    def transmit_to(self, window_title):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            self.capture_area = {
                "left": window.left,
                "top": window.top,
                "width": window.width,
                "height": window.height
            }
            self.save_settings()
        except IndexError:
            print(f"Janela '{window_title}' não encontrada.")

    def start_selection(self):
        self.selection_mode = True
        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.selection_start_x = event.x_root
        self.selection_start_y = event.y_root

    def on_drag(self, event):
        if self.selection_mode:
            self.selection_end_x = event.x_root
            self.selection_end_y = event.y_root
            self.draw_selection_rectangle()

    def on_release(self, event):
        if self.selection_mode:
            self.selection_mode = False
            self.selection_end_x = event.x_root
            self.selection_end_y = event.y_root
            self.draw_selection_rectangle()
            self.update_capture_area()
            self.clear_selection_rectangle()
            self.root.unbind("<ButtonPress-1>")
            self.root.unbind("<B1-Motion>")
            self.root.unbind("<ButtonRelease-1>")
            self.save_settings()

    def draw_selection_rectangle(self):
        self.clear_selection_rectangle()
        self.selection_rectangle = tk.Canvas(self.root, highlightthickness=2, highlightbackground="red")
        self.selection_rectangle.place(x=min(self.selection_start_x, self.selection_end_x), y=min(self.selection_start_y, self.selection_end_y), width=abs(self.selection_end_x - self.selection_start_x), height=abs(self.selection_end_y - self.selection_start_y))

    def clear_selection_rectangle(self):
        if self.selection_rectangle:
            self.selection_rectangle.destroy()
            self.selection_rectangle = None

    def update_capture_area(self):
        left = min(self.selection_start_x, self.selection_end_x)
        top = min(self.selection_start_y, self.selection_end_y)
        width = abs(self.selection_end_x - self.selection_start_x)
        height = abs(self.selection_end_y - self.selection_start_y)
        self.capture_area = {"left": left, "top": top, "width": width, "height": height}

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def update_opacity(self, value):
        self.root.attributes('-alpha', value)
        self.save_settings()

    def close(self):
        self.save_settings()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SSAMight(root)
    root.mainloop()