import os
import glob

directory = 'd:/snapticle-media'
updated_count = 0

# Process HTML files
for filepath in glob.glob(os.path.join(directory, '**', '*.html'), recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'SnapTicle' in content:
        content = content.replace('SnapTicle', 'Snapticle')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML: {filepath}")
        updated_count += 1

# Process Python files
for filepath in glob.glob(os.path.join(directory, '**', '*.py'), recursive=True):
    if 'fix_typo.py' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'SnapTicle' in content:
        content = content.replace('SnapTicle', 'Snapticle')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated Python: {filepath}")
        updated_count += 1

print(f"Total files updated: {updated_count}")
