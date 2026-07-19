import re

def update_gsap():
    path = r'd:\snapticle-media\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the GSAP script
    script_start = '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>\n<script>\n  gsap.registerPlugin(ScrollTrigger);\n\n  // Advanced Scroll Animations\n  document.addEventListener("DOMContentLoaded", () => {'
    
    if script_start not in content:
        print("Could not find exact script start. Checking alternative...")
        script_start = 'document.addEventListener("DOMContentLoaded", () => {'

    # Find the end of the script
    script_end_pattern = r'  \}\);\n</script>\n\n</body>'
    match = re.search(script_end_pattern, content)
    if not match:
        print("Could not find script end.")
        return
    
    end_idx = match.start() + len('  });\n</script>')
    start_idx = content.find(script_start)

    new_gsap_code = """<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
<script>
  gsap.registerPlugin(ScrollTrigger);

  document.addEventListener("DOMContentLoaded", () => {
    // 1. Process Tracker Animation
    const processSteps = gsap.utils.toArray('.depth-card');
    const trackerSteps = document.querySelectorAll('.process-step');
    
    if (processSteps.length > 0 && trackerSteps.length > 0) {
      processSteps.forEach((step, i) => {
        ScrollTrigger.create({
          trigger: step,
          start: "top center",
          end: "bottom center",
          onEnter: () => activateStep(i),
          onEnterBack: () => activateStep(i),
        });
      });

      function activateStep(index) {
        trackerSteps.forEach((t, i) => {
          const indicator = t.querySelector('.indicator');
          const innerDot = t.querySelector('.inner-dot');
          const label = t.querySelector('.label');
          
          if (i === index) {
            gsap.to(indicator, { backgroundColor: '#1f2f2a', borderColor: '#d8b496', scale: 1.1, duration: 0.3 });
            gsap.to(innerDot, { backgroundColor: '#ffffff', duration: 0.3 });
            gsap.to(label, { opacity: 1, color: '#b05f22', duration: 0.3 });
          } else if (i < index) {
            gsap.to(indicator, { backgroundColor: '#b05f22', borderColor: '#ffffff', scale: 1, duration: 0.3 });
            gsap.to(innerDot, { backgroundColor: '#ffffff', duration: 0.3 });
            gsap.to(label, { opacity: 0.8, color: '#2f231b', duration: 0.3 });
          } else {
            gsap.to(indicator, { backgroundColor: '#f8efe1', borderColor: '#ffffff', scale: 1, duration: 0.3 });
            gsap.to(innerDot, { backgroundColor: 'rgba(0,0,0,0.2)', duration: 0.3 });
            gsap.to(label, { opacity: 0.5, color: '#2f231b', duration: 0.3 });
          }
        });
      }
    }

    // 2. Global Staggered 3D Reveals
    const revealSections = document.querySelectorAll('.reveal-on-scroll');
    revealSections.forEach(section => {
      gsap.fromTo(section, 
        { y: 60, opacity: 0, rotationX: -25, transformPerspective: 1000 },
        {
          y: 0, 
          opacity: 1,
          rotationX: 0,
          duration: 1,
          ease: "power3.out",
          scrollTrigger: {
            trigger: section,
            start: "top 85%",
            toggleActions: "play none none reverse"
          }
        }
      );
    });

    // 3. Interactive 3D Tilt Cards
    const cards = document.querySelectorAll('.reveal-card, .depth-card');
    cards.forEach(card => {
      card.style.transformStyle = "preserve-3d";
      const icon = card.querySelector('svg');
      if (icon) icon.style.transform = "translateZ(40px)";

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left; 
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -12; // Max 12 deg
        const rotateY = ((x - centerX) / centerX) * 12;
        
        gsap.to(card, {
          rotateX: rotateX,
          rotateY: rotateY,
          duration: 0.4,
          ease: "power2.out",
          transformPerspective: 1000
        });
      });
      card.addEventListener('mouseleave', () => {
        gsap.to(card, {
          rotateX: 0,
          rotateY: 0,
          duration: 0.7,
          ease: "power2.out"
        });
      });
    });

    // 4. Z-Axis Scroll Depth for Glass Containers
    const glassContainers = document.querySelectorAll('#features .border-white\\\\/5, #faq .border-white\\\\/5');
    glassContainers.forEach(container => {
      gsap.fromTo(container,
        { scale: 0.92, opacity: 0.4, rotationX: 10, transformPerspective: 1200 },
        {
          scale: 1, opacity: 1, rotationX: 0,
          duration: 1.2,
          ease: "power2.out",
          scrollTrigger: {
            trigger: container,
            start: "top 95%",
            end: "top 35%",
            scrub: 1
          }
        }
      );
    });

    // 5. Continuous Floating 3D Icons
    const floatIcons = document.querySelectorAll('.reveal-card svg, .depth-card svg');
    floatIcons.forEach((icon, i) => {
      gsap.to(icon, {
        y: -8,
        rotationY: 15,
        rotationX: 10,
        duration: 3 + (i % 2),
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
      });
    });

    // 6. Magnetic Hover Effect for primary buttons
    const magneticButtons = document.querySelectorAll('a.bg-\\\\[\\\\#111915\\\\], a.bg-\\\\[\\\\#b05f22\\\\], a.bg-\\\\[\\\\#e63946\\\\]');
    magneticButtons.forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = (e.clientX - rect.left - rect.width / 2) * 0.3;
        const y = (e.clientY - rect.top - rect.height / 2) * 0.3;
        gsap.to(btn, { x: x, y: y, duration: 0.2, ease: "power2.out" });
      });
      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: "elastic.out(1, 0.3)" });
      });
    });
  });
</script>"""

    # We need to find the exact replacement bounds based on start_idx
    # Let's search back to <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js">
    script_block_start = content.rfind('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>', 0, start_idx + 100)
    
    if script_block_start != -1:
        new_content = content[:script_block_start] + new_gsap_code + content[end_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated GSAP successfully.")
    else:
        print("Could not find exact bounds.")

if __name__ == '__main__':
    update_gsap()
