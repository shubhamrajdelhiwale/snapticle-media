import os
import glob
import re

def main():
    html_files = glob.glob(r'd:\snapticle-media\*.html')
    
    for file in html_files:
        if "index.html" in file:
            continue # Already manually updated
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Replace the favicon logo used in service navbars with the new logo
        content = re.sub(
            r'<img src="favicon-32x32\.png"',
            r'<img src="MyLogo_trimmed.png"',
            content
        )
        
        # 2. Replace any other references to snapticle-logo.png
        # We don't add the text wrapper here because it might break white navbars.
        content = re.sub(
            r'<img src="snapticle-logo\.png"',
            r'<img src="MyLogo_trimmed.png"',
            content
        )
        
        # 3. Replace the footer logo (which is snapticle-logo-footer.png) with the new logo AND the text wrapper
        def footer_replacement(match):
            return (
                '<div class="flex items-center gap-3 mb-4 w-fit">\n'
                '        <img src="MyLogo_trimmed.png" alt="Snapticle Media Logo" class="h-14 w-auto object-contain">\n'
                '        <span class="text-white font-bold text-xl tracking-wide">Snapticle Media</span>\n'
                '      </div>'
            )
            
        content = re.sub(
            r'<img src="snapticle-logo-footer\.png"[^>]*>',
            footer_replacement,
            content
        )
        
        if content != original_content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {os.path.basename(file)}")

if __name__ == '__main__':
    main()
