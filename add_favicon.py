import os
import glob

html_files = glob.glob('d:/snapticle-media/*.html')
favicon_tag = '    <link rel="icon" href="favicon-32x32.png">\n'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Check if favicon already exists
    has_favicon = any('favicon' in line.lower() for line in lines)
    if has_favicon:
        continue
        
    # Insert after <head>
    for i, line in enumerate(lines):
        if '<head>' in line.lower():
            lines.insert(i + 1, favicon_tag)
            break
            
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

print(f"Checked {len(html_files)} files.")
