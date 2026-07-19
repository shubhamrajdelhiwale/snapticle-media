import os
import re

def update_form():
    path = r'd:\snapticle-media\form.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove "Section X — " text from all headings
    # e.g., "Section 1 &mdash; About You" -> "About You"
    # Note: &mdash; is used in the HTML.
    content = re.sub(r'Section \d+ &mdash; ', '', content)
    
    # Also remove "Section 8 &mdash; Final Step" if it varies
    
    # 2. Add 3D effect CSS classes
    # We will inject a new 3D style into the <style> block
    style_injection = """
  /* 3D Hover Effects */
  .form-section {
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    transform-style: preserve-3d;
  }
  .form-section:hover {
    transform: translateY(-10px) rotateX(2deg) rotateY(-1deg);
    box-shadow: -10px 20px 40px rgba(255, 204, 204, 0.15), 
                inset 2px 2px 5px rgba(255,255,255,0.1), 
                inset -2px -2px 5px rgba(0,0,0,0.5);
    border-color: rgba(255, 204, 204, 0.4);
  }
"""
    # Insert styles before the closing </style> tag in the custom block
    if "/* Success screen */" in content and "/* 3D Hover Effects */" not in content:
        content = content.replace("/* Success screen */", style_injection + "\n  /* Success screen */")
        
    # 3. Replace the dark burgundy #5E0819 with light pink #FFCCCC
    # Note: case insensitive replacement just in case
    content = re.sub(r'#5E0819', '#FFCCCC', content, flags=re.IGNORECASE)
    
    # Fix contrast: the button text is white, which is hard to read on #FFCCCC.
    # The submit button has `text-white`
    # Let's change `text-white` on the submit button to `text-black`
    submit_btn_regex = r'(<button type="submit"[^>]*?)text-white([^>]*>)'
    content = re.sub(submit_btn_regex, r'\1text-black\2', content)

    # Change the hover variant for the button: from hover:bg-[#7b0a21] to something like hover:bg-[#ffb3b3]
    content = content.replace('hover:bg-[#7b0a21]', 'hover:bg-[#ffb3b3]')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Updated form.html successfully!")

if __name__ == '__main__':
    update_form()
