import re

def process_file():
    filepath = r'd:\snapticle-media\index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_hero = False
    in_fixed_bg = False
    new_lines = []

    for line in lines:
        if '<section id="home"' in line:
            in_hero = True
        
        # Check for the start of the fixed background I added earlier
        if '<div class="fixed inset-0 pointer-events-none z-[-1]' in line:
            in_fixed_bg = True
            continue
            
        if in_fixed_bg:
            if '</div>' in line and not 'blur-[' in line:
                in_fixed_bg = False
            continue
        
        if 'blur-3xl' in line:
            if not in_hero:
                continue
                
        if '</section>' in line:
            in_hero = False

        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_file()
    print("Done")
