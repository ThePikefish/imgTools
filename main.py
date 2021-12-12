
import tkinter as tk
from tkinter import Button, Label, image_types, ttk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import cv2


# Init tkinter window
win = tk.Tk()
win.title("imgTools")
win.geometry("1000x600")

# Image label
image_container = tk.Canvas(win, borderwidth=2, relief="groove")
image_container.grid(row=0, column=0, columnspan=2)

img = None
contrast_val = 1

def update_image():
    global img, adapted_img, contrast_val
    img.thumbnail((350, 350))
    contrast = ImageEnhance.Contrast(img)
    imgMod = contrast.enhance((contrast_val/50))
    adapted_img = ImageTk.PhotoImage(imgMod)
    image_container.create_image(0, 0, image=adapted_img, anchor="nw")


def open_image():
    global img
    try:
        img = Image.open("test.jpg")
        update_image()
    except:
        print("hello")
        pass

open_button = Button(text="Avaa kuva", command=open_image)
open_button.grid(row=1, column=0, columnspan=2)


def change_contrast(var):
    global img, contrast_val
    contrast_val = int(var)
    update_image()


bright = tk.Label(win, text="Kirkkaus:")
bright.grid(row=0, column=1, columnspan=2, sticky="e")
v1 = tk.IntVar()
scale_contrast = tk.Scale(win, from_=0, to=100, variable=v1, orient="horizontal", command=change_contrast)
scale_contrast.set(50)
scale_contrast.grid(row=0, column=1, sticky="e")


win.columnconfigure(1, weight=1)
win.rowconfigure(0, weight=1)


win.mainloop()