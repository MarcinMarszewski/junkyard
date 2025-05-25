import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

width, height = 320, 240
running = True

ambient = 0.4
shininess = 40
specular = 300
diffuse = 1
color_r = 180
color_g = 100
color_b = 60

def calculate_color(x, y, frame):
    cx, cy = width // 2, height // 2
    radius = 60 

    lx = cx + int(80 * np.cos(frame * 0.07))
    ly = cy + int(80 * np.sin(frame * 0.07))
    lz = 100

    dx = x - cx
    dy = y - cy
    dist2 = dx * dx + dy * dy

    if dist2 <= radius * radius:
        z = np.sqrt(radius * radius - dx * dx - dy * dy)
        nx, ny, nz = dx / radius, dy / radius, z / radius

        lx_dir = lx - x
        ly_dir = ly - y
        lz_dir = lz - z
        l_len = np.sqrt(lx_dir ** 2 + ly_dir ** 2 + lz_dir ** 2)
        lx_dir /= l_len
        ly_dir /= l_len
        lz_dir /= l_len

        diff = max(0, nx * lx_dir + ny * ly_dir + nz * lz_dir)
        
        reflect = 2 * (nx * lx_dir + ny * ly_dir + nz * lz_dir) * np.array([nx, ny, nz]) - np.array([lx_dir, ly_dir, lz_dir])
        reflect_len = np.sqrt(np.sum(reflect ** 2))
        if reflect_len != 0:
            reflect /= reflect_len

        light_factor = (ambient + diffuse * diff) + specular * max(0, reflect[2]) ** shininess
        r = int(min(255, color_r * light_factor))
        g = int(min(255, color_g * light_factor))
        b = int(min(255, color_b * light_factor))
    else:
        r, g, b = 20, 20, 30

    return (r, g, b)

def on_key(event):
    global running
    if event.keysym == 'Escape':
        root.destroy()
    elif event.keysym == 'space':
        running = not running
    elif event.keysym == '1':
        global ambient, shininess, specular, diffuse
        ambient = min(1.0, ambient + 0.1)

root = tk.Tk()
label = tk.Label(root)
label.pack()
root.bind('<Key>', on_key)

def show_frame(frame=0):
    if not running:
        root.after(50, show_frame, frame)
        return
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            img_array[y, x] = calculate_color(x, y, frame)
    img = Image.fromarray(img_array, 'RGB')
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img
    root.after(50, show_frame, frame + 1)

show_frame()
root.mainloop()