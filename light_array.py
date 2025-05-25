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

def calculate_frame(frame):
    cx, cy = width // 2, height // 2
    radius = 60

    lx = cx + int(80 * np.cos(frame * 0.07))
    ly = cy + int(80 * np.sin(frame * 0.07))
    lz = 100

    y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    dx = x - cx
    dy = y - cy
    dist2 = dx**2 + dy**2

    mask = dist2 <= radius**2

    z = np.zeros_like(dx, dtype=np.float32)
    z[mask] = np.sqrt(radius**2 - dx[mask]**2 - dy[mask]**2)

    nx = np.zeros_like(dx, dtype=np.float32)
    ny = np.zeros_like(dy, dtype=np.float32)
    nz = np.zeros_like(z, dtype=np.float32)
    nx[mask] = dx[mask] / radius
    ny[mask] = dy[mask] / radius
    nz[mask] = z[mask] / radius

    lx_dir = lx - x
    ly_dir = ly - y
    lz_dir = lz - z
    lx_dir = lx_dir.astype(np.float32)
    ly_dir = ly_dir.astype(np.float32)
    lz_dir = lz_dir.astype(np.float32)
    l_len = np.sqrt(lx_dir**2 + ly_dir**2 + lz_dir**2)
    lx_dir /= l_len
    ly_dir /= l_len
    lz_dir /= l_len

    diff = np.zeros_like(dx, dtype=np.float32)
    diff[mask] = np.maximum(0, nx[mask] * lx_dir[mask] + ny[mask] * ly_dir[mask] + nz[mask] * lz_dir[mask])

    reflect = np.zeros((height, width, 3), dtype=np.float32)
    dot = np.zeros_like(dx, dtype=np.float32)
    dot[mask] = nx[mask] * lx_dir[mask] + ny[mask] * ly_dir[mask] + nz[mask] * lz_dir[mask]
    reflect[mask, 0] = 2 * dot[mask] * nx[mask] - lx_dir[mask]
    reflect[mask, 1] = 2 * dot[mask] * ny[mask] - ly_dir[mask]
    reflect[mask, 2] = 2 * dot[mask] * nz[mask] - lz_dir[mask]
    reflect_len = np.sqrt(np.sum(reflect**2, axis=2))
    reflect[mask] /= reflect_len[mask][..., None]

    spec = np.zeros_like(dx, dtype=np.float32)
    spec[mask] = np.maximum(0, reflect[mask, 2]) ** shininess

    light_factor = np.zeros_like(dx, dtype=np.float32)
    light_factor[mask] = (ambient + diffuse * diff[mask]) + specular * spec[mask]

    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    img_array[..., 0] = np.where(mask, np.clip(color_r * light_factor, 0, 255), 20)
    img_array[..., 1] = np.where(mask, np.clip(color_g * light_factor, 0, 255), 20)
    img_array[..., 2] = np.where(mask, np.clip(color_b * light_factor, 0, 255), 30)

    return img_array

def on_key(event):
    global running
    if event.keysym == 'Escape':
        root.destroy()
    elif event.keysym == 'space':
        running = not running
    elif event.keysym == '1': #gold
        global ambient, shininess, specular, diffuse, color_r, color_g, color_b
        ambient = 0.24725
        diffuse = 0.75164
        specular = 0.628281
        shininess = 51.2
        color_r = 239
        color_g = 191
        color_b = 4
    elif event.keysym == '2': #black rubber
        ambient = 0.02
        diffuse = 0.01
        specular = 0.4
        shininess = 10
        color_r = 70
        color_g = 70
        color_b = 70
    elif event.keysym == '3': #polished gold
        ambient = 0.24725
        diffuse = 0.34615
        specular = 0.797357
        shininess = 83.2
        color_r = 239
        color_g = 191
        color_b = 4
    elif event.keysym == '4': #silver
    elif event.keysym == '5': #bronze
    elif event.keysym == '6': #chrome
    elif event.keysym == '7': #copper
    elif event.keysym == '8': #polished copper



root = tk.Tk()
label = tk.Label(root)
label.pack()
root.bind('<Key>', on_key)

def show_frame(frame=0):
    if not running:
        root.after(50, show_frame, frame)
        return
    img_array = calculate_frame(frame)
    img = Image.fromarray(img_array, 'RGB')
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img
    root.after(50, show_frame, frame + 1)

show_frame()
root.mainloop()