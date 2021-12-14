
import tkinter as tk
from tkinter import StringVar, ttk, Button, Label, image_types, filedialog
from tkinter import messagebox
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk, ImageFilter, ImageEnhance

# Init tkinter window
win = tk.Tk()
win.title("imgTools")
win.geometry("1280x720")

style = ttk.Style()
style.theme_use('clam')

# Toolbar
toolbar = tk.Frame(win, background="#262626", height=20)
statusbar = tk.Frame(win, background="#262626", height=10)
main = tk.PanedWindow(win, background="#282828")

toolbar.pack(side="top", fill="x")
statusbar.pack(side="bottom", fill="x")
main.pack(side="top", fill="both", expand=True)

# Left and right panes
left_pane = tk.Frame(main, background="#282828", width=500)
right_pane = tk.PanedWindow(main, background="#373737", width=200)
main.add(left_pane, stretch="always")
main.add(right_pane, stretch="always")

notebook = tk.Frame(right_pane, background="#373737", height=70)
right_pane.add(notebook, stretch="always")

# Image container
image_container = tk.Canvas(left_pane, borderwidth=10, relief="groove", height="600", width="1000", background="#282828")

image_container.pack()

img = None
contrast_val = 50
brightness_val = 50
sharpness_val = 0
sharpness_radius_val = 10
sharpness_threshold_val = 6
saturation_val = 50
blur_val = 0
scale_length = 200
quality_val = 95


# Update image
def update_image(img, save=False):
    global preview_img, contrast_val, brightness_val, sharpness_val, saturation_val, blur_val, sharpness_radius_val, sharpness_threshold_val
    if img == None:
        return

    width, height = img.size
    # Apply values to image
    imgMod = ImageEnhance.Contrast(img).enhance(contrast_val/50)
    imgMod = ImageEnhance.Brightness(imgMod).enhance(brightness_val/50)
    sharpness = int((sharpness_val/50) * 100)
    sharpness_threshold_val = int(sharpness_threshold_val*(width/2200))
    imgMod = imgMod.filter(ImageFilter.UnsharpMask(radius=sharpness_radius_val*width/20000, percent=sharpness, threshold=sharpness_threshold_val))
    imgMod = ImageEnhance.Color(imgMod).enhance(saturation_val/50)
    imgMod = imgMod.filter(ImageFilter.GaussianBlur(blur_val*width/5000))

    # Apply to thumbnail or final
    if (save == False):
        preview_img = ImageTk.PhotoImage(imgMod)
        image_container.create_image(0, 0, image=preview_img, anchor="nw")
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
        messagebox.showerror("Virhe", "Kuvan lataamisessa oli virhe.")
        pass

open_button = ttk.Button(toolbar, text="Avaa kuva", command=open_image)
open_button.pack(side="left")


# Save image
def save_image():
    global img, filename
    if img:
        ext = StringVar()
        filetypes = (("JPEG", ("*.jpg", "*.jpeg", "*.jpe")), ("PNG", "*.png"), ("TIFF", "*.tiff"))
        name = filedialog.asksaveasfilename(initialfile="Untitled", title="Valitse tiedosto", typevariable=ext, filetypes=filetypes)
        if name:
            img = Image.open(filename)
            final = update_image(img, True)
            final.save(name + "." + ext.get().lower(), quality=quality_val, subsampling=0)

save_button = ttk.Button(toolbar, text="Tallenna kuva", command=save_image)
save_button.pack(side="left")


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

# Sharpness
def change_sharpness(var):
    global img, sharpness_val
    if img:
        sharpness_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Sharpness radius
def change_sharpness_radius(var):
    global img, sharpness_radius_val
    if img:
        sharpness_radius_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Sharpness threshold
def change_sharpness_threshold(var):
    global img, sharpness_threshold_val
    if img:
        sharpness_threshold_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Saturation
def change_saturation(var):
    global img, saturation_val
    if img:
        saturation_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Blur
def change_blur(var):
    global img, blur_val
    if img:
        blur_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Quality
def change_quality(var):
    global quality_val
    quality_val = int(var)



vcontrast = tk.IntVar()
scale_contrast = tk.Scale(right_pane, label="Kontrasti", from_=0, to=100, length=scale_length, variable=vcontrast, orient="horizontal", command=change_contrast, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_contrast.set(50)
scale_contrast.pack()

vbrightness = tk.IntVar()
scale_brightness = tk.Scale(right_pane, label="Kirkkaus", from_=0, to=100, length=scale_length, variable=vbrightness, orient="horizontal", command=change_brightness, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_brightness.set(50)
scale_brightness.pack()

vsharpness = tk.IntVar()
scale_sharpness = tk.Scale(right_pane, label="Terävöinti", from_=0, to=100, length=scale_length, variable=vsharpness, orient="horizontal", command=change_sharpness, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_sharpness.set(0)
scale_sharpness.pack()

vsharpness_radius = tk.IntVar()
scale_sharpness_radius = tk.Scale(right_pane, label="Terävöinti tarkkuus", from_=0, to=100, length=scale_length, variable=vsharpness_radius, orient="horizontal", command=change_sharpness_radius, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_sharpness_radius.set(10)
scale_sharpness_radius.pack()

vsharpness_threshold = tk.IntVar()
scale_sharpness_threshold = tk.Scale(right_pane, label="Terävöinti kynnys", from_=0, to=100, length=scale_length, variable=vsharpness_threshold, orient="horizontal", command=change_sharpness_threshold, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_sharpness_threshold.set(6)
scale_sharpness_threshold.pack()

vsaturation = tk.IntVar()
scale_saturation = tk.Scale(right_pane, label="Värikylläisyys", from_=0,  to=100, length=scale_length, variable=vsaturation, orient="horizontal", command=change_saturation, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_saturation.set(50)
scale_saturation.pack()

vblur = tk.IntVar()
scale_blur = tk.Scale(right_pane, label="Sumennus", from_=0,  to=100, length=scale_length, variable=vblur, orient="horizontal", command=change_blur, bg="#454545", troughcolor="#555555", highlightbackground="#303030")
scale_blur.set(0)
scale_blur.pack()

vquality = tk.IntVar()
scale_quality = tk.Scale(toolbar, label="Kompressiolaatu", from_=0,  to=100, length=scale_length, variable=vquality, command=change_quality, orient="horizontal",  bg="#454545", troughcolor="#303030", highlightbackground="#303030")
scale_quality.set(95)
scale_quality.pack(side="left")

win.mainloop()