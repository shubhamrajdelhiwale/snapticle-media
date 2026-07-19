import os
import glob

html_files = glob.glob('d:/snapticle-media/*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop Nav
    content = content.replace(
        '<a href="snapticle-media-social-media-management.html" class="block px-6 py-3 hover:bg-gray-50">Social Media Management</a>',
        '<a href="snapticle-media-social-media-services.html" class="block px-6 py-3 hover:bg-gray-50">Social Media Services</a>'
    )

    # Mobile Nav
    content = content.replace(
        '<a href="snapticle-media-social-media-management.html" class="block py-1 border-b border-gray-50">Social Media Management</a>',
        '<a href="snapticle-media-social-media-services.html" class="block py-1 border-b border-gray-50">Social Media Services</a>'
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(html_files)} HTML files.")
