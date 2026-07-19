import os
import glob

html_files = glob.glob('d:/snapticle-media/*.html')

count = 0
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'snapticle-media-services.html' in content:
        content = content.replace('snapticle-media-services.html', 'snapticle-media-social-media-services.html')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Fixed link in {count} HTML files.")
