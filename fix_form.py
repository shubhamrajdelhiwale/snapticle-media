import os
import re

def fix_form():
    path = r'd:\snapticle-media\form.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the numbering so it's fully visible and not cut off.
    # Currently: class="absolute -top-10 -right-10 text-[#FFCCCC]/10 text-9xl font-black pointer-events-none"
    # Change to: class="absolute top-2 right-6 text-[#FFCCCC]/10 text-8xl font-black pointer-events-none"
    content = re.sub(
        r'class="absolute -top-10 -right-10 text-\[#FFCCCC\]/10 text-9xl font-black pointer-events-none"',
        'class="absolute top-2 right-6 text-[#FFCCCC]/10 text-8xl font-black pointer-events-none"',
        content
    )
    
    # 2. Add custom dropdown CSS and JS
    custom_dropdown_css = """
  /* Custom Dropdown Styles */
  .custom-dropdown {
    position: relative;
    width: 100%;
  }
  .custom-dropdown-selected {
    width: 100%;
    background: transparent;
    border-bottom: 2px solid rgba(255,255,255,0.1);
    color: white;
    padding: 12px 0;
    font-size: 1.1rem;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
  }
  .custom-dropdown-selected:hover, .custom-dropdown.active .custom-dropdown-selected {
    border-bottom-color: #FFCCCC;
  }
  .custom-dropdown.active .custom-dropdown-selected i {
    transform: rotate(180deg);
  }
  .custom-dropdown-options {
    position: absolute;
    top: calc(100% + 5px);
    left: 0;
    width: 100%;
    background: #1a1a1a;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    z-index: 100;
    max-height: 250px;
    overflow-y: auto;
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px);
    transition: all 0.3s ease;
  }
  .custom-dropdown.active .custom-dropdown-options {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
  .custom-dropdown-option {
    padding: 12px 20px;
    color: #e5e7eb;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .custom-dropdown-option:hover {
    background: rgba(255, 204, 204, 0.15);
    color: #FFCCCC;
  }
  .custom-dropdown-option.selected {
    background: rgba(255, 204, 204, 0.2);
    color: #FFCCCC;
    font-weight: bold;
  }
  /* Scrollbar for dropdown */
  .custom-dropdown-options::-webkit-scrollbar {
    width: 6px;
  }
  .custom-dropdown-options::-webkit-scrollbar-track {
    background: transparent;
  }
  .custom-dropdown-options::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
    border-radius: 10px;
  }
  .custom-dropdown-options::-webkit-scrollbar-thumb:hover {
    background: rgba(255,255,255,0.3);
  }
"""
    if "/* Custom Dropdown Styles */" not in content:
        content = content.replace('/* Form Specific Styles */', custom_dropdown_css + '\n  /* Form Specific Styles */')

    custom_dropdown_js = """
    // Custom Dropdown Initialization
    const selects = document.querySelectorAll('select.custom-select');
    selects.forEach(select => {
      // Hide original select
      select.style.display = 'none';
      
      // Create wrapper
      const wrapper = document.createElement('div');
      wrapper.className = 'custom-dropdown';
      select.parentNode.insertBefore(wrapper, select);
      wrapper.appendChild(select);
      
      // Create selected display
      const selectedDiv = document.createElement('div');
      selectedDiv.className = 'custom-dropdown-selected';
      selectedDiv.innerHTML = `<span class="selected-text text-gray-500">${select.options[select.selectedIndex].text}</span> <i class="fa-solid fa-chevron-down text-sm transition-transform duration-300 text-gray-400"></i>`;
      wrapper.appendChild(selectedDiv);
      
      // Create options list
      const optionsDiv = document.createElement('div');
      optionsDiv.className = 'custom-dropdown-options';
      wrapper.appendChild(optionsDiv);
      
      // Populate options
      Array.from(select.options).forEach((option, index) => {
        if (index === 0 && option.disabled) return; // Skip placeholder
        
        const optionEl = document.createElement('div');
        optionEl.className = 'custom-dropdown-option';
        optionEl.textContent = option.text;
        
        optionEl.addEventListener('click', () => {
          // Update original select
          select.selectedIndex = index;
          select.dispatchEvent(new Event('change')); // Trigger change event if needed
          
          // Update selected text
          const textSpan = selectedDiv.querySelector('.selected-text');
          textSpan.textContent = option.text;
          textSpan.classList.remove('text-gray-500');
          textSpan.classList.add('text-white'); // Change color when selected
          
          // Highlight selected option
          Array.from(optionsDiv.children).forEach(child => child.classList.remove('selected'));
          optionEl.classList.add('selected');
          
          // Close dropdown
          wrapper.classList.remove('active');
        });
        optionsDiv.appendChild(optionEl);
      });
      
      // Toggle dropdown on click
      selectedDiv.addEventListener('click', (e) => {
        e.stopPropagation();
        // Close others
        document.querySelectorAll('.custom-dropdown').forEach(d => {
          if (d !== wrapper) d.classList.remove('active');
        });
        wrapper.classList.toggle('active');
      });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
      document.querySelectorAll('.custom-dropdown').forEach(d => d.classList.remove('active'));
    });
"""
    if "// Custom Dropdown Initialization" not in content:
        content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "document.addEventListener('DOMContentLoaded', () => {\n" + custom_dropdown_js)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Fixed numbering and dropdowns successfully!")

if __name__ == '__main__':
    fix_form()
