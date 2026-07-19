import sys

def apply_redesign():
    path = r'd:\snapticle-media\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Grid alignments
    content = content.replace('lg:grid-cols-[0.98fr_1.02fr]', 'lg:grid-cols-[1fr_1.15fr]')
    content = content.replace('lg:grid-cols-[0.92fr_1.08fr]', 'lg:grid-cols-[1fr_1.15fr]')
    content = content.replace('lg:grid-cols-[0.9fr_1.1fr]', 'lg:grid-cols-[1fr_1.15fr]')

    # 2. Typography
    content = content.replace('<h2 class="mt-5 max-w-xl text-4xl font-black tracking-tight text-white sm:text-5xl">', 
                              '<h2 class="mt-5 max-w-xl text-5xl font-black tracking-tight text-white lg:text-6xl">')
    content = content.replace('<h2 class="mt-5 text-4xl font-black tracking-tight text-white sm:text-5xl">', 
                              '<h2 class="mt-5 text-5xl font-black tracking-tight text-white lg:text-6xl">')
    content = content.replace('<h2 class="mt-5 text-4xl font-black tracking-tight sm:text-5xl">', 
                              '<h2 class="mt-5 text-5xl font-black tracking-tight sm:text-6xl">')

    # 3. Padding & Containers
    # Process
    content = content.replace('<section id="process" class="reveal-on-scroll relative py-12 lg:py-20">',
                              '<section id="process" class="reveal-on-scroll relative py-20 lg:py-28">')
    # Features
    content = content.replace('<section id="features" class="reveal-on-scroll relative py-12 lg:py-20">\n  <div class="mx-auto max-w-7xl px-6">',
                              '<section id="features" class="reveal-on-scroll relative py-10 lg:py-14">\n  <div class="mx-4 lg:mx-8 rounded-[3rem] border border-white/5 bg-white/[0.02] py-20 lg:py-28">\n    <div class="mx-auto max-w-7xl px-6">')
    # Close Features container before the next section
    content = content.replace('</section>\n\n<section class="reveal-on-scroll relative overflow-hidden py-28 text-white sm:py-32"',
                              '  </div>\n</section>\n\n<section class="reveal-on-scroll relative overflow-hidden py-28 text-white sm:py-32"')

    # FAQ
    content = content.replace('<section id="faq" class="reveal-on-scroll relative py-12 lg:py-20 text-white">\n  <div class="mx-auto max-w-7xl px-6">',
                              '<section id="faq" class="reveal-on-scroll relative py-10 lg:py-14 text-white">\n  <div class="mx-4 lg:mx-8 rounded-[3rem] border border-white/5 bg-white/[0.02] py-20 lg:py-28">\n    <div class="mx-auto max-w-7xl px-6">')
    # Close FAQ container before CTA
    content = content.replace('</section>\n\n<section class="reveal-on-scroll relative py-12 lg:py-20 text-white lg:py-24">',
                              '  </div>\n</section>\n\n<section class="reveal-on-scroll relative py-20 lg:py-28 text-white">')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    apply_redesign()
