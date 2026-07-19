import sys

def process():
    path = r'd:\snapticle-media\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    in_hidden = False
    
    for i, line in enumerate(lines):
        if line.strip() == '<div class="hidden">':
            in_hidden = True
            
        if in_hidden:
            if line.strip() == '</div>' and i > 2000:
                in_hidden = False
            continue
            
        new_lines.append(line)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
if __name__ == '__main__':
    process()
