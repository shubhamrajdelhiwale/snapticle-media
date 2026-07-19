import re

def fix_footer():
    path = r'd:\snapticle-media\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the first footer
    start_str = '<footer class="relative overflow-hidden pb-8 pt-12 text-white">'
    start_idx = content.find(start_str)
    
    # Find the end of the broken footer block
    end_str = '<!-- BG SHAPE -->\n\n</footer>\n\n</div>'
    end_idx = content.find(end_str) + len(end_str)

    if start_idx == -1 or end_idx == -1:
        print("Could not find the footer block!")
        return

    # Build the new unified footer
    new_footer = """
<footer class="w-[98%] mx-auto mt-20 mb-4 rounded-[2.5rem] border border-white/5 bg-white/[0.02] p-10 lg:p-16 text-white backdrop-blur-xl relative overflow-hidden">
  <div class="pointer-events-none absolute inset-x-0 bottom-0 h-64 bg-gradient-to-t from-[#e63946]/5 to-transparent"></div>
  
  <div class="relative z-10 grid gap-12 lg:grid-cols-[2fr_1fr_1fr_1fr]">
    <!-- Brand -->
    <div class="space-y-6">
      <img src="snapticle-logo.png" alt="Snapticle Media" class="h-10 w-auto object-contain filter brightness-0 invert transition hover:scale-105">
      <p class="max-w-sm text-sm leading-7 text-gray-400">
        Snapticle Media builds marketing pages that feel premium, move with purpose, and make it easy for visitors to take the next step.
      </p>
      <div class="flex gap-4 text-lg text-gray-400">
        <a href="https://www.facebook.com/profile.php?id=61589602650498" class="hover:text-[#e63946] transition"><i class="fa-brands fa-facebook"></i></a>
        <a href="https://x.com/snapticlemedia" class="hover:text-[#e63946] transition"><i class="fa-brands fa-x-twitter"></i></a>
        <a href="https://www.linkedin.com/company/snapticlemedia" class="hover:text-[#e63946] transition"><i class="fa-brands fa-linkedin"></i></a>
        <a href="https://www.youtube.com/@snapticlemedia" class="hover:text-[#e63946] transition"><i class="fa-brands fa-youtube"></i></a>
        <a href="https://www.instagram.com/snapticlemedia" class="hover:text-[#e63946] transition"><i class="fa-brands fa-instagram"></i></a>
      </div>
    </div>

    <!-- Links -->
    <div>
      <h3 class="font-bold text-white mb-6 uppercase tracking-wider text-sm">Company</h3>
      <ul class="space-y-3 text-sm text-gray-400">
        <li><a href="#home" class="hover:text-[#e63946] transition">Home</a></li>
        <li><a href="#process" class="hover:text-[#e63946] transition">Process</a></li>
        <li><a href="#features" class="hover:text-[#e63946] transition">Features</a></li>
        <li><a href="#faq" class="hover:text-[#e63946] transition">FAQ</a></li>
      </ul>
    </div>

    <!-- Services -->
    <div>
      <h3 class="font-bold text-white mb-6 uppercase tracking-wider text-sm">Services</h3>
      <ul class="space-y-3 text-sm text-gray-400">
        <li><a href="snapticle-media-social-media-services.html" class="hover:text-[#e63946] transition">Social Media Services</a></li>
        <li><a href="snapticle-media-content-shoot-services.html" class="hover:text-[#e63946] transition">Content & Shoot</a></li>
        <li><a href="snapticle-media-graphics-designing.html" class="hover:text-[#e63946] transition">Graphics & Designing</a></li>
        <li><a href="snapticle-media-website-development.html" class="hover:text-[#e63946] transition">Website Development</a></li>
        <li><a href="snapticle-media-seo-automation.html" class="hover:text-[#e63946] transition">SEO & Automation</a></li>
        <li><a href="snapticle-media-tools-software-hub.html" class="hover:text-[#e63946] transition">Tools & Software</a></li>
      </ul>
    </div>

    <!-- Office -->
    <div>
      <h3 class="font-bold text-white mb-6 uppercase tracking-wider text-sm">Our Office</h3>
      <div class="space-y-3 text-sm text-gray-400">
        <p class="font-medium text-white">Snapticle Media</p>
        <p>Sector 62, Noida,<br>Uttar Pradesh 201309</p>
        <p class="text-[#e63946] font-semibold mt-4">📞 +91-9863113682</p>
        <p class="text-xs mt-1 opacity-70">Serving across Noida, Delhi NCR & India</p>
      </div>
    </div>
  </div>

  <div class="relative z-10 mt-16 pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-gray-500">
    <div>&copy; 2026 Snapticle Media | by Efsolit Technology Private Limited</div>
    <div class="flex gap-4">
      <a href="snapticle-media-privacy.html" class="hover:text-white transition">Privacy Policy</a>
      <a href="snapticle-media-terms.html" class="hover:text-white transition">Terms of Service</a>
    </div>
  </div>
</footer>

</div>"""

    new_content = content[:start_idx] + new_footer + content[end_idx:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Footer replaced successfully.")

if __name__ == '__main__':
    fix_footer()
