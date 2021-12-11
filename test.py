from PIL import Image
print("Hauki on kala!")

img = Image.open("test.jpg")
img.save("test.tiff")