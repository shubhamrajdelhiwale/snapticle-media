import re

def update_hover_effects():
    # 1. Update style.css
    css_path = r'd:\snapticle-media\style.css'
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    liquid_css = """
/* Liquid fill hover button effect */
.btn-liquid {
  position: relative;
  overflow: hidden;
  z-index: 1;
}
.btn-liquid::before {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  width: 300%;
  height: 300%;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 40%;
  transform: translate(-50%, 0) rotate(0deg);
  transition: top 0.7s cubic-bezier(0.22, 1, 0.36, 1);
  animation: liquidWave 6s linear infinite;
  z-index: -1;
  pointer-events: none;
}
.btn-liquid:hover::before {
  top: -80%;
}
@keyframes liquidWave {
  0% { transform: translate(-50%, 0) rotate(0deg); }
  100% { transform: translate(-50%, 0) rotate(360deg); }
}

/* Link hover sweep */
.link-sweep {
  position: relative;
}
.link-sweep::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #e63946;
  transition: width 0.3s ease;
}
.link-sweep:hover::after {
  width: 100%;
}
"""
    if '.btn-liquid' not in css_content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(liquid_css)

    # 2. Update index.html
    html_path = r'd:\snapticle-media\index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Apply link-sweep to desktop nav links
    for link in ["Home", "Services", "Portfolio", "Blog", "About Us", "Contact Us"]:
        target = f'class="transition hover:text-[#e63946]">{link}</a>'
        replacement = f'class="transition hover:text-[#e63946] link-sweep">{link}</a>'
        html_content = html_content.replace(target, replacement)

    # Apply btn-liquid to primary buttons
    # 1. Nav button
    target1 = 'class="rounded-full bg-[#e63946] px-5 py-3 text-sm font-semibold text-white shadow-[0_18px_45px_rgba(230,57,70,0.18)] transition hover:-translate-y-0.5 hover:bg-[#d32f2f]">Get Free Quote</a>'
    rep1 = target1.replace('class="', 'class="btn-liquid ')
    html_content = html_content.replace(target1, rep1)

    # 2. Hero button
    target2 = 'class="inline-flex items-center justify-center gap-2 rounded-full bg-[#e63946] px-7 py-4 text-base font-semibold text-white shadow-[0_18px_45px_rgba(230,57,70,0.2)] transition duration-300 hover:-translate-y-1 hover:shadow-[0_24px_55px_rgba(230,57,70,0.28)] hover:bg-[#d32f2f]">'
    rep2 = target2.replace('class="', 'class="btn-liquid ')
    html_content = html_content.replace(target2, rep2)

    # 3. Bottom CTA
    target3 = 'class="inline-flex items-center justify-center rounded-full bg-[#e63946] px-8 py-4 text-sm font-bold text-white shadow-[0_0_30px_rgba(230,57,70,0.3)] transition duration-300 hover:-translate-y-1 hover:shadow-[0_0_45px_rgba(230,57,70,0.5)] hover:bg-[#ff4d5a]">'
    rep3 = target3.replace('class="', 'class="btn-liquid ')
    html_content = html_content.replace(target3, rep3)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    update_hover_effects()
