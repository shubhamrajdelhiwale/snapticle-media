import rembg
from PIL import Image
import io

def process_logo():
    input_path = r'd:\snapticle-media\MyLogo.PNG'
    output_path = r'd:\snapticle-media\MyLogo_trimmed.png'
    
    # 1. Remove background
    with open(input_path, 'rb') as i:
        input_data = i.read()
        
    output_data = rembg.remove(input_data)
    
    # 2. Trim empty space
    img = Image.open(io.BytesIO(output_data))
    
    # Get bounding box of non-zero alpha
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, 'PNG')
    print("Background removed and image trimmed perfectly!")

if __name__ == "__main__":
    process_logo()
