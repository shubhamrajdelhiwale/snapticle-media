import os
import glob

html_files = glob.glob('d:/snapticle-media/*.html')

count = 0
for file in html_files:
    if os.path.basename(file) == 'index.html':
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    old_header_logo = '<img src="favicon-32x32.png" alt="Snapticle Media Logo" class="w-12 h-12 object-contain">'
    new_header_logo = '<img src="MyLogo_trimmed.png" alt="Snapticle Media Logo" class="h-10 lg:h-11 w-auto object-contain lg:pl-2">'
    
    if old_header_logo in content:
        content = content.replace(old_header_logo, new_header_logo)
        modified = True

    old_footer_logo = '<img src="snapticle-logo-footer.png" class="h-14 mb-4">'
    new_footer_logo = '<img src="MyLogo_trimmed.png" alt="Snapticle Media" class="h-14 w-auto object-contain mb-4">'
    
    if old_footer_logo in content:
        content = content.replace(old_footer_logo, new_footer_logo)
        modified = True

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Updated logos in {count} HTML files.")
