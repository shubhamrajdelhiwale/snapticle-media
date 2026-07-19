import glob
import re

def main():
    html_files = glob.glob('*.html')
    
    for filepath in html_files:
        if filepath == 'index.html':
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # If it's a light theme page
        if '<body class="bg-gray-50"' in content or '<body class="bg-white"' in content or filepath == 'form.html':
            # Fix header backgrounds that might be rendering incorrectly as light
            content = re.sub(
                r'bg-gradient-to-r from-slate-900 to-slate-800 text-white',
                'bg-slate-100 text-slate-900 border-b border-gray-200',
                content
            )
            
            # Replace text-white with text-slate-900
            content = content.replace('text-white', 'text-slate-900')
            
            # Revert for buttons and specific components that SHOULD be white text on dark
            content = content.replace('bg-orange-500 text-slate-900', 'bg-orange-500 text-white')
            content = content.replace('bg-[#A6213D] text-slate-900', 'bg-[#A6213D] text-white')
            content = content.replace('bg-[#1e1b4b] text-slate-900', 'bg-[#1e1b4b] text-white')
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed colors in {filepath}")

if __name__ == '__main__':
    main()
