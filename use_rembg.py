import rembg
from PIL import Image

def remove_background():
    input_path = r'C:\Users\adars\.gemini\antigravity-ide\brain\82e8a99a-a633-4a3d-b4e1-73cd5150f782\character_laptop_1784232738639.png'
    output_path = r'd:\snapticle-media\guy-laptop.png'
    
    with open(input_path, 'rb') as i:
        input_data = i.read()
        
    output_data = rembg.remove(input_data)
    
    with open(output_path, 'wb') as o:
        o.write(output_data)
        
    print("Background removed perfectly with rembg!")

if __name__ == "__main__":
    remove_background()
