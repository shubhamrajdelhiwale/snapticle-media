import os
import glob
import re

def main():
    html_files = glob.glob(r'd:\snapticle-media\*.html')
    css_files = glob.glob(r'd:\snapticle-media\*.css')
    
    for file in html_files + css_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Replace hex codes
        content = re.sub(r'#e63946', '#5E0819', content, flags=re.IGNORECASE)
        content = re.sub(r'#ff4d5a', '#5E0819', content, flags=re.IGNORECASE)
        
        # 2. Replace RGB values (230, 57, 70 is #e63946)
        # 94, 8, 25 is #5E0819
        content = re.sub(r'rgba\(230,\s*57,\s*70,', 'rgba(94,8,25,', content)
        content = re.sub(r'rgb\(230,\s*57,\s*70\)', 'rgb(94,8,25)', content)
        
        # 3. Replace Tailwind classes (e.g. -pink-500, -pink-50)
        # Matches any prefix ending with a dash, e.g., 'bg-', 'text-', 'hover:bg-', 'from-', 'to-'
        content = re.sub(r'(-)?pink-\d{2,3}', r'\1[#5E0819]', content)
        
        # 4. In service pages, the brand name Snapticle used text-red-500. We want to align this too.
        content = re.sub(r'text-red-500', r'text-[#5E0819]', content)
        
        if content != original_content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {os.path.basename(file)}")

if __name__ == '__main__':
    main()
