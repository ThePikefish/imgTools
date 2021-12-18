
##  imgTools
#   Toolbox for image manipulation
#   by: Kristo Jonsson
#   https://github.com/ThePikefish/imgTools


import tkinter as tk
from tkinter import StringVar, ttk, Button, Label, image_types, filedialog
from tkinter import messagebox
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

# Settings
img = None
brightness_val = 50
contrast_val = 50
saturation_val = 50
sharpness_val = 0
sharpness_radius_val = 10
sharpness_threshold_val = 6
blur_val = 0
scale_length = 200
mirrored = False
rotate_val = False
quality_val = 95

scale_style = {
    "from_":        0,
    "to":           100,
    "length":       scale_length,
    "sliderlength": 20,
    "orient":       "horizontal",
    "fg":           "#A2A2A2",
    "bg":           "#454545",
    "troughcolor":  "#303030",
    "activebackground":"#A2A2A2",
    "highlightbackground":"#303030",
    "bd":           1,
    "relief":       "flat"
}


# Init tkinter window
win = tk.Tk()
win.title("imgTools")
win.geometry("1280x720")

style = ttk.Style()
style.theme_use('clam')

# Toolbar, statusbar, main
toolbar = tk.Frame(win, background="#373737", height=20)
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
image_container = tk.Canvas(left_pane, borderwidth=10, height="600", width="1000", background="#282828", highlightbackground="#282828")
image_container.pack()

# Button style
button_style = ttk.Style()
button_style.theme_use("alt")
button_style.configure("TButton", background="#454545", foreground="#A2A2A2")
button_style.map("TButton", background=[("active", "#A2A2A2")], foreground=[("active", "black")])


# Update image
def update_image(img, save=False):
    global preview_img, contrast_val, brightness_val, sharpness_val, saturation_val, blur_val, sharpness_radius_val, sharpness_threshold_val, mirrored
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
    if mirrored:
        imgMod = imgMod.transpose(Image.FLIP_LEFT_RIGHT)
    if rotate_val != 0:
        if rotate_val == 90:
            imgMod = imgMod.transpose(Image.ROTATE_90)
        if rotate_val == 180:
            imgMod = imgMod.transpose(Image.ROTATE_180)
        if rotate_val == 270:
            imgMod = imgMod.transpose(Image.ROTATE_270)

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
open_button.pack(side="left", fill="y", ipadx=10, pady=5, padx=5)


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
save_button.pack(side="left", fill="y", ipadx=10, pady=5, padx=5)

# Brightness
def change_brightness(var):
    global img, brightness_val
    if img:
        brightness_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Contrast
def change_contrast(var):
    global img, contrast_val
    if img:
        contrast_val = int(var)
        img.thumbnail((1000, 600))
        update_image(img)

# Saturation
def change_saturation(var):
    global img, saturation_val
    if img:
        saturation_val = int(var)
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

# Mirror
def mirror():
    global img, mirrored
    if img:
        if mirrored == False:
            mirrored = True
        else:
            mirrored = False
        img.thumbnail((1000, 600))
        update_image(img)

# Rotate
def rotate():
    global img, rotate_val
    if img:
        rotate_val = rotate_val + 90
        if rotate_val > 270:
            rotate_val = 0
        img.thumbnail((1000, 600))
        update_image(img)

# Tool buttons
mirror_button = ttk.Button(toolbar, text="Peilikuva", command=mirror)
mirror_button.pack(side="right", fill="y", ipadx=10, pady=5, padx=5)

rotate_button = ttk.Button(toolbar, text="Käännä 90", command=rotate)
rotate_button.pack(side="right", fill="y", ipadx=10, pady=5, padx=5)

# Sliders
vbrightness = tk.IntVar()
scale_brightness = tk.Scale(right_pane, label="Kirkkaus", variable=vbrightness, command=change_brightness, **scale_style)
scale_brightness.set(brightness_val)
scale_brightness.pack()

vcontrast = tk.IntVar()
scale_contrast = tk.Scale(right_pane, label="Kontrasti", variable=vcontrast, command=change_contrast, **scale_style)
scale_contrast.set(contrast_val)
scale_contrast.pack()

vsaturation = tk.IntVar()
scale_saturation = tk.Scale(right_pane, label="Värikylläisyys", variable=vsaturation, command=change_saturation, **scale_style)
scale_saturation.set(saturation_val)
scale_saturation.pack()

vsharpness = tk.IntVar()
scale_sharpness = tk.Scale(right_pane, label="Terävöinti", variable=vsharpness, command=change_sharpness, **scale_style)
scale_sharpness.set(sharpness_val)
scale_sharpness.pack()

vsharpness_radius = tk.IntVar()
scale_sharpness_radius = tk.Scale(right_pane, label="Terävöinti tarkkuus", variable=vsharpness_radius, command=change_sharpness_radius, **scale_style)
scale_sharpness_radius.set(sharpness_radius_val)
scale_sharpness_radius.pack()

vsharpness_threshold = tk.IntVar()
scale_sharpness_threshold = tk.Scale(right_pane, label="Terävöinti kynnys", variable=vsharpness_threshold, command=change_sharpness_threshold, **scale_style)
scale_sharpness_threshold.set(sharpness_threshold_val)
scale_sharpness_threshold.pack()

vblur = tk.IntVar()
scale_blur = tk.Scale(right_pane, label="Sumennus", variable=vblur, command=change_blur, **scale_style)
scale_blur.set(blur_val)
scale_blur.pack()

vquality = tk.IntVar()
scale_quality = tk.Scale(toolbar, label="Kompressiolaatu", variable=vquality, command=change_quality, **scale_style)
scale_quality.set(quality_val)
scale_quality.pack(side="left", ipadx=10, pady=5, padx=5)


win.mainloop()