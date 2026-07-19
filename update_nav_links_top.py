import os
import glob

html_files = glob.glob('d:/snapticle-media/*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define replacements
    replacements = [
        (
            '<button class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors" aria-haspopup="true" aria-expanded="false">\n          Services',
            '<a href="snapticle-media-services.html" class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors" aria-haspopup="true" aria-expanded="false">\n          Services'
        ),
        (
            '<button class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          Portfolio',
            '<a href="snapticle-media-portfolio.html" class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          Portfolio'
        ),
        (
            '<button class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          Blog',
            '<a href="snapticle-media-blog.html" class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          Blog'
        ),
        (
            '<button class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          About Us',
            '<a href="snapticle-media-overview.html" class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          About Us'
        ),
        (
            '<button class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          Contact Us',
            '<a href="snapticle-media-contact.html" class="flex items-center gap-1 font-medium hover:text-orange-500 transition-colors">\n          Contact Us'
        )
    ]

    modified = False
    for old_str, new_str in replacements:
        if old_str in content:
            content = content.replace(old_str, new_str)
            modified = True

    # After replacing the opening tags, we need to replace the corresponding </button> tags with </a>
    # Since these are specific to the desktop nav, we can find them by looking for the closing button tag right after the SVG
    if modified:
        content = content.replace('></path></svg>\n        </button>', '></path></svg>\n        </a>')

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"Checked {len(html_files)} HTML files.")
