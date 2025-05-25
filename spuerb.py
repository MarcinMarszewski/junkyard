import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

width, height = 320, 240
running = True

ambient = [0.329412,0.223529,0.027451]
diffuse = [0.780392,0.568627,0.113725]
specular = [0.992157,0.941176,0.807843]
shininess = 27.8974

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

    light_factor_r = np.zeros_like(dx, dtype=np.float32)
    light_factor_g = np.zeros_like(dx, dtype=np.float32)
    light_factor_b = np.zeros_like(dx, dtype=np.float32)
    light_factor_r[mask] = (ambient[0] + diffuse[0] * diff[mask]) + specular[0] * spec[mask]
    light_factor_g[mask] = (ambient[1] + diffuse[1] * diff[mask]) + specular[1] * spec[mask]
    light_factor_b[mask] = (ambient[2] + diffuse[2] * diff[mask]) + specular[2] * spec[mask]

    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    img_array[..., 0] = np.where(mask, np.clip(255 * light_factor_r, 0, 255), 20)
    img_array[..., 1] = np.where(mask, np.clip(255 * light_factor_g, 0, 255), 20)
    img_array[..., 2] = np.where(mask, np.clip(255 * light_factor_b, 0, 255), 30)

    return img_array

def on_key(event):
    global running
    if event.keysym == 'Escape':
        root.destroy()
    elif event.keysym == 'space':
        running = not running
    elif event.keysym == '1': #brass
        global ambient, shininess, specular, diffuse
        ambient = [0.329412,0.223529,0.027451]
        diffuse = [0.780392,0.568627,0.113725]
        specular = [0.992157,0.941176,0.807843]
        shininess = 27.8974
    elif event.keysym == '2': #bronze
        ambient = [0.2125,0.1275,0.054]
        diffuse = [0.714,0.4284,0.18144]
        specular = [0.393548,0.271906,0.166721]
        shininess = 25.6
    elif event.keysym == '3': #polished bronze
        ambient = [0.25,0.148,0.06475]
        diffuse = [0.4,0.2368,0.1036]
        specular = [0.774597,0.458561,0.200621]
        shininess = 76.8
    elif event.keysym == '4': #chrome
        ambient = [0.25,0.25,0.25]
        diffuse = [0.4,0.4,0.4]
        specular = [0.774597,0.774597,0.774597]
        shininess = 76.8
    elif event.keysym == '5': #copper
        ambient = [0.19125,0.0735,0.0225]
        diffuse = [0.7038,0.27048,0.0828]
        specular = [0.256777,0.137622,0.086014]
        shininess = 12.8
    elif event.keysym == '6': #polished copper
        ambient = [0.2295,0.08825,0.0275]
        diffuse = [0.5508,0.2118,0.066]
        specular = [0.580594,0.223257,0.0695701]
        shininess = 51.2
    elif event.keysym == '7': #gold
        ambient = [0.24725,0.1995,0.0745]
        diffuse = [0.75164,0.60648,0.22648]
        specular = [0.628281,0.555802,0.366065]
        shininess = 51.2
    elif event.keysym == '8': #polished gold
        ambient = [0.24725,0.2245,0.0645]
        diffuse = [0.34615,0.3143,0.0903]
        specular = [0.797357,0.723991,0.208006]
        shininess = 83.2
    elif event.keysym == '9': #black plastic
        ambient = [0.0,0.0,0.0]
        diffuse = [0.01,0.01,0.01]
        specular = [0.50,0.50,0.50]
        shininess = 32
    elif event.keysym == '0': #black rubber
        ambient = [0.02,0.02,0.02]
        diffuse = [0.01,0.01,0.01]
        specular = [0.4,0.4,0.4]
        shininess = 10
    
        


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
    img = img.resize((width * 3, height * 3), resample=Image.NEAREST)
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img
    root.after(50, show_frame, frame + 1)

show_frame()
root.mainloop()