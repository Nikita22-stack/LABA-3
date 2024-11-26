import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.image1_path = None
        self.image2_path = None

    def create_widgets(self):
        self.frame_top = tk.Frame(self, bg="#f0f0f0")
        self.frame_top.pack(fill="x")

        self.block1 = tk.Button(self.frame_top, text="Открыть изображение 1", bg="#ffffff", width=20, height=5, command=self.on_click_block1)
        self.block1.pack(side="left", padx=10, pady=10)

        self.block2 = tk.Button(self.frame_top, text="Открыть изображение 2", bg="#ffffff", width=20, height=5, command=self.on_click_block2)
        self.block2.pack(side="left", padx=10, pady=10)

        self.button_process = tk.Button(self, text="Обработать", bg="#ffffff", width=20, height=5, command=self.process)
        self.button_process.pack(pady=20)

    def on_click_block1(self):
        self.image1_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image1_path:
            self.block1.config(text=os.path.basename(self.image1_path))

    def on_click_block2(self):
        self.image2_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image2_path:
            self.block2.config(text=os.path.basename(self.image2_path))

    def process(self):
        if self.image1_path and self.image2_path:
            output_filename = os.path.basename(self.image1_path).split('.')[0] + '_output.jpg'
            output_path = os.path.join(os.getcwd(), output_filename)
            self.process_images(self.image1_path, self.image2_path, output_path)

    def process_images(self, image1_path, image2_path, output_path):
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)
        
        # Записать в канал насыщенности синус тона
        image1_hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
        image1_hsv[..., 1] = np.sin(image1_hsv[..., 1])
        image1 = cv2.cvtColor(image1_hsv, cv2.COLOR_HSV2BGR)
        
        # Накладывание изображений с эффектом Мягкий свет
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        if np.mean(image2_gray) < 128:
            blending_mode = "darken"
        else:
            blending_mode = "screen"
        
        if blending_mode == "darken":
            result = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
        else:
            result = cv2.addWeighted(image1, 0.5, image2, 0.5, 255)
        
        cv2.imwrite(output_path, result)

root = tk.Tk()
root.title("Обработка изображений")
app = Application(master=root)
app.mainloop()
