
import tkinter as tk
from tkinter import StringVar, ttk, Button, Label, image_types, filedialog
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk, ImageFilter, ImageEnhance


# Init tkinter window
win = tk.Tk()
win.title("imgTools")
win.geometry("1280x720")

# Image container
image_container = tk.Canvas(win, borderwidth=10, relief="groove", height="600", width="1000")
image_container.grid(row=0, column=0, columnspan=2)

img = None
contrast_val = 50
brightness_val = 50


# Update image
def update_image(img, save=False):
    global adapted_img, contrast_val, brightness_val
    if img == None:
        return

    # Edited values
    #contrast = ImageEnhance.Contrast(img)
    #brightness = ImageEnhance.Brightness(img)

    #imgMod = contrast.enhance((contrast_val/50))
    #imgMod = brightness.enhance((1))
    imgMod = ImageEnhance.Contrast(img).enhance(contrast_val/50)
    imgMod = ImageEnhance.Brightness(imgMod).enhance(brightness_val/50)
    if (save == False):
        adapted_img = ImageTk.PhotoImage(imgMod)
        image_container.create_image(0, 0, image=adapted_img, anchor="nw")
    else:
        return imgMod

# Open image
def open_image():
    global img, filename
    try:
        filename = filedialog.askopenfilename()
        img = Image.open(filename)
        img.thumbnail((1000, 600))
        update_image(img)
    except:
        print("hello")
        pass

open_button = Button(text="Avaa kuva", command=open_image)
open_button.grid(row=1, column=0, columnspan=1, sticky="w")


# Save image
def save_image():
    global img, filename
    if img:
        ext = StringVar()
        filetypes = (("JPEG", ("*.jpg", "*.jpeg", "*.jpe")), ("PNG", "*.png"), ("TIFF", "*.tiff"))
        name = filedialog.asksaveasfilename(initialfile="Untitled", title="Valitse tiedosto", typevariable=ext, filetypes=filetypes)
        if name:
            img = Image.open(filename)
            #final = apply_changes(img)
            final = update_image(img, True)
            final.save(name + "." + ext.get().lower())

save_button = Button(text="Tallenna kuva", command=save_image)
save_button.grid(row=1, column=1, columnspan=1, sticky="w")


# Contrast
def change_contrast(var):
    global img, contrast_val
    if img:
        contrast_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Brightness
def change_brightness(var):
    global img, brightness_val
    if img:
        brightness_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)



v1 = tk.IntVar()
scale_contrast = tk.Scale(win, from_=0, to=100, variable=v1, orient="horizontal", command=change_contrast)
scale_contrast.set(50)
scale_contrast.grid(row=0, column=1, sticky="e")

v2 = tk.IntVar()
scale_brightness = tk.Scale(win, from_=0, to=100, variable=v2, orient="horizontal", command=change_brightness)
scale_brightness.set(50)
scale_brightness.grid(row=1, column=1, sticky="e")


win.columnconfigure(1, weight=1)
win.rowconfigure(0, weight=1)


win.mainloop()