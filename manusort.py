import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Your categories
categories = ["Good", "Bad", "Delete", "Not Meme"]

# Folders
input_folder = filedialog.askdirectory(title="Select your meme folder")
output_folder = filedialog.askdirectory(title="Select where to save sorted memes")

# Prepare category folders
for category in categories:
    os.makedirs(os.path.join(output_folder, category), exist_ok=True)

# Load images
images = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
current_idx = 0

# Main app
root = tk.Tk()
root.title("Meme Sorter")

img_label = tk.Label(root)
img_label.pack()

def show_image():
    global img_label
    if current_idx >= len(images):
        img_label.config(text="All memes sorted! 🎉")
        return
    img_path = os.path.join(input_folder, images[current_idx])
    img = Image.open(img_path)
    img.thumbnail((800, 800))
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

def move_image(category):
    global current_idx
    if current_idx >= len(images):
        return
    src = os.path.join(input_folder, images[current_idx])
    dst = os.path.join(output_folder, category, images[current_idx])
    shutil.move(src, dst)
    current_idx += 1
    show_image()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()

for cat in categories:
    btn = tk.Button(button_frame, text=cat, width=15, command=lambda c=cat: move_image(c))
    btn.pack(side="left", padx=5, pady=5)

# Hotkeys
def key_handler(event):
    keys = {
        '1': categories[0],
        '2': categories[1],
        '3': categories[2],
        '4': categories[3],
        '5': categories[4],
        '6': categories[5],
        '7': categories[6],
        '8': categories[7],
    }
    if event.char in keys:
        move_image(keys[event.char])

root.bind('<Key>', key_handler)

show_image()
root.mainloop()
