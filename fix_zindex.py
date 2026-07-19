import os

def fix_zindex():
    path = r'd:\snapticle-media\form.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to add JS that adjusts the z-index of the parent form-section
    # In the JS:
    # wrapper.classList.toggle('active');
    # We can add logic:
    # const parentSection = wrapper.closest('.form-section');
    # if (wrapper.classList.contains('active')) {
    #     parentSection.style.zIndex = '50';
    # } else {
    #     parentSection.style.zIndex = '';
    # }
    
    js_to_replace = """        wrapper.classList.toggle('active');"""
    new_js = """        wrapper.classList.toggle('active');
        const parentSection = wrapper.closest('.form-section');
        if (parentSection) {
          if (wrapper.classList.contains('active')) {
            parentSection.style.zIndex = '50';
          } else {
            parentSection.style.zIndex = '1';
          }
        }"""
    
    content = content.replace(js_to_replace, new_js)
    
    # Also need to reset z-index when clicking outside
    js_outside = """    document.addEventListener('click', () => {
      document.querySelectorAll('.custom-dropdown').forEach(d => d.classList.remove('active'));
    });"""
    new_js_outside = """    document.addEventListener('click', () => {
      document.querySelectorAll('.custom-dropdown').forEach(d => {
        d.classList.remove('active');
        const parentSection = d.closest('.form-section');
        if (parentSection) parentSection.style.zIndex = '1';
      });
    });"""
    
    content = content.replace(js_outside, new_js_outside)
    
    # And when clicking an option
    js_option = """          // Close dropdown
          wrapper.classList.remove('active');"""
    new_js_option = """          // Close dropdown
          wrapper.classList.remove('active');
          const parentSection = wrapper.closest('.form-section');
          if (parentSection) parentSection.style.zIndex = '1';"""
          
    content = content.replace(js_option, new_js_option)

    # Let's ensure all .form-section elements default to z-index: 1 so the stacking context is consistent
    if "/* 3D Hover Effects */" in content:
        content = content.replace(".form-section {", ".form-section {\n    z-index: 1;\n    position: relative;")
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Fixed z-index stacking context for dropdowns!")

if __name__ == '__main__':
    fix_zindex()
