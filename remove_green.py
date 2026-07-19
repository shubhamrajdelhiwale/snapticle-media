from PIL import Image
import numpy as np
import sys

def remove_green(image_path, output_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        data = np.array(img)
        
        # Simple chroma key for bright green
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        
        # Green is dominant
        mask = (g > 120) & (r < 120) & (b < 120) & (g > r * 1.5) & (g > b * 1.5)
        
        data[mask, 3] = 0
        
        out_img = Image.fromarray(data)
        out_img.save(output_path)
        print("Success")
    except Exception as e:
        print("Error:", e)

remove_green(r'C:\Users\adars\.gemini\antigravity-ide\brain\82e8a99a-a633-4a3d-b4e1-73cd5150f782\character_laptop_1784232738639.png', r'd:\snapticle-media\guy-laptop.png')
