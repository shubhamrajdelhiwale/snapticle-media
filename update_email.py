import os
import glob

html_files = glob.glob('d:/snapticle-media/*.html')

count = 0
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'snapticlemedia@gmail.com' in content:
        content = content.replace('snapticlemedia@gmail.com', 'contact@snapticlemedia.in')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Updated email in {count} HTML files.")
