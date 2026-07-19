import os

def build_form():
    with open(r'd:\snapticle-media\index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    header_end_idx = content.find('</header>') + len('</header>')
    header = content[:header_end_idx]

    footer_start_idx = content.find('<footer')
    footer_end = content.find('</body>')
    footer = content[footer_start_idx:footer_end]
    scripts = content[footer_end:]

    # Add GSAP for form animations
    form_styles = """
<style>
  /* Form Specific Styles */
  .form-input {
    width: 100%;
    background: transparent;
    border: none;
    border-bottom: 2px solid rgba(255,255,255,0.1);
    color: white;
    padding: 12px 0;
    font-size: 1.1rem;
    outline: none;
    transition: all 0.3s ease;
  }
  .form-input:focus {
    border-bottom-color: #5E0819;
    box-shadow: 0 4px 15px rgba(94,8,25,0.2);
  }
  .form-label {
    position: absolute;
    left: 0;
    top: 12px;
    color: #9ca3af;
    font-size: 1.1rem;
    pointer-events: none;
    transition: all 0.3s ease;
  }
  .form-input:focus ~ .form-label,
  .form-input:not(:placeholder-shown) ~ .form-label {
    top: -12px;
    font-size: 0.85rem;
    color: #5E0819;
  }
  
  .pill-checkbox input[type="checkbox"] {
    display: none;
  }
  .pill-checkbox span {
    display: inline-block;
    padding: 10px 20px;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.05);
    color: #d1d5db;
  }
  .pill-checkbox input[type="checkbox"]:checked + span {
    background: #5E0819;
    border-color: #5E0819;
    color: white;
    box-shadow: 0 0 20px rgba(94,8,25,0.5);
    transform: scale(1.05);
  }
  
  .radio-card input[type="radio"] {
    display: none;
  }
  .radio-card .card-content {
    border: 2px solid rgba(255,255,255,0.1);
    border-radius: 1rem;
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.03);
    text-align: center;
  }
  .radio-card input[type="radio"]:checked + .card-content {
    border-color: #5E0819;
    background: rgba(94,8,25,0.15);
    box-shadow: 0 0 25px rgba(94,8,25,0.4);
    transform: translateY(-5px);
  }

  .custom-select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    background-size: 1.2rem;
  }
  
  /* Success screen */
  #success-screen {
    display: none;
    opacity: 0;
  }
  
  /* Select Option text color for dropdowns so it's visible */
  option {
    background: #111111;
    color: white;
  }
</style>
"""

    main_content = """
<main class="pt-32 pb-24 px-6 lg:px-8 relative min-h-screen z-10">
  <!-- Decorative background elements -->
  <div class="pointer-events-none absolute left-0 top-1/4 h-96 w-96 rounded-full bg-[#5E0819]/10 blur-[120px]"></div>
  <div class="pointer-events-none absolute right-0 bottom-1/4 h-96 w-96 rounded-full bg-[#5E0819]/10 blur-[120px]"></div>

  <div class="max-w-4xl mx-auto">
    
    <!-- HEADER TEXT -->
    <div class="text-center mb-16 form-section">
      <h1 class="text-4xl lg:text-6xl font-black text-white mb-6 tracking-tight">🚀 Let's Build Something <span class="text-[#5E0819]">Great.</span></h1>
      <p class="text-lg text-gray-400 max-w-2xl mx-auto">Tell us about your business and goals. We'll get back to you with the best solution tailored for your growth.</p>
    </div>

    <!-- SUCCESS SCREEN (Hidden by default) -->
    <div id="success-screen" class="text-center py-20">
      <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-[#5E0819]/20 text-[#5E0819] text-5xl mb-8 shadow-[0_0_50px_rgba(94,8,25,0.4)]">
        <i class="fa-solid fa-check"></i>
      </div>
      <h2 class="text-4xl font-bold text-white mb-4">Thank You!</h2>
      <p class="text-xl text-gray-300 mb-2">We've received your enquiry.</p>
      <p class="text-gray-400 mb-12">Our team will review your requirements and reach out within 24 hours.<br>Meanwhile, feel free to explore our portfolio.</p>
      
      <div class="flex flex-col sm:flex-row justify-center gap-6">
        <a href="snapticle-media-portfolio.html" class="inline-block border border-white/20 rounded-full px-8 py-4 font-semibold hover:border-white transition-all text-white hover:bg-white/5">View Portfolio</a>
        <a href="https://wa.me/919863113682" target="_blank" class="inline-flex items-center justify-center gap-2 bg-[#25D366] text-white rounded-full px-8 py-4 font-semibold shadow-[0_10px_30px_rgba(37,211,102,0.3)] hover:scale-105 transition-all">
          <i class="fa-brands fa-whatsapp text-xl"></i> WhatsApp Us
        </a>
      </div>
    </div>

    <!-- THE FORM -->
    <form id="project-form" class="space-y-16 relative" action="https://formsubmit.co/contact@snapticlemedia.in" method="POST">
      <!-- Hidden configs for FormSubmit -->
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_subject" value="New Project Enquiry - Snapticle Media">
      <!-- We will prevent default on submit and use AJAX -->

      <!-- SECTION 1: ABOUT YOU -->
      <section class="form-section p-8 lg:p-12 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-10 -right-10 text-[#5E0819]/10 text-9xl font-black pointer-events-none">01</div>
        <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Section 1 &mdash; About You</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="relative mt-2">
            <input type="text" id="fullname" name="Full Name" required placeholder=" " class="form-input">
            <label for="fullname" class="form-label">Full Name *</label>
          </div>
          <div class="relative mt-2">
            <input type="text" id="company" name="Company Name" required placeholder=" " class="form-input">
            <label for="company" class="form-label">Company / Brand Name *</label>
          </div>
          <div class="relative mt-2">
            <input type="email" id="email" name="Work Email" required placeholder=" " class="form-input">
            <label for="email" class="form-label">Work Email *</label>
          </div>
          <div class="relative mt-2">
            <input type="tel" id="phone" name="Phone Number" required placeholder=" " class="form-input">
            <label for="phone" class="form-label">Phone Number *</label>
          </div>
          <div class="relative mt-2">
            <input type="url" id="website" name="Website" placeholder=" " class="form-input">
            <label for="website" class="form-label">Website (Optional)</label>
          </div>
          <div class="relative mt-2">
            <input type="text" id="city" name="City/Country" placeholder=" " class="form-input">
            <label for="city" class="form-label">City / Country</label>
          </div>
        </div>
      </section>

      <!-- SECTION 2: YOUR BUSINESS -->
      <section class="form-section p-8 lg:p-12 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-10 -right-10 text-[#5E0819]/10 text-9xl font-black pointer-events-none">02</div>
        <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Section 2 &mdash; Your Business</h3>
        
        <div class="relative">
          <label class="block text-gray-300 mb-4 font-semibold text-lg">Which best describes your business?</label>
          <select name="Business Type" required class="form-input custom-select text-white font-medium pb-2 border-b-2 border-white/20 focus:border-[#5E0819]">
            <option value="" disabled selected>Select an option</option>
            <option value="Startup">Startup</option>
            <option value="Small Business">Small Business</option>
            <option value="Enterprise">Enterprise</option>
            <option value="Personal Brand">Personal Brand</option>
            <option value="E-commerce">E-commerce</option>
            <option value="Restaurant / Cafe">Restaurant / Cafe</option>
            <option value="Hotel / Resort">Hotel / Resort</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Real Estate">Real Estate</option>
            <option value="Education">Education</option>
            <option value="Fashion">Fashion</option>
            <option value="Beauty">Beauty</option>
            <option value="Technology">Technology</option>
            <option value="Finance">Finance</option>
            <option value="Manufacturing">Manufacturing</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </section>

      <!-- SECTION 3: HELP NEEDED -->
      <section class="form-section p-8 lg:p-12 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-10 -right-10 text-[#5E0819]/10 text-9xl font-black pointer-events-none">03</div>
        <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Section 3 &mdash; Help Needed</h3>
        
        <label class="block text-gray-300 mb-6 font-semibold text-lg">What do you need help with? (Select all that apply)</label>
        <div class="flex flex-wrap gap-4">
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Website Design & Development"><span>Website Design & Development</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Branding & Identity"><span>Branding & Identity</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Social Media Management"><span>Social Media Management</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Content Creation"><span>Content Creation</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Lead Generation"><span>Lead Generation</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Customer Retention"><span>Customer Retention</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Performance Marketing"><span>Performance Marketing</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="SEO & Google Business"><span>SEO & Google Business</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="AI & CRM Automation"><span>AI & CRM Automation</span></label>
          <label class="pill-checkbox"><input type="checkbox" name="Help[]" value="Strategy & Consultation"><span>Strategy & Consultation</span></label>
        </div>
      </section>

      <!-- SECTION 4: PROJECT DETAILS -->
      <section class="form-section p-8 lg:p-12 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-10 -right-10 text-[#5E0819]/10 text-9xl font-black pointer-events-none">04</div>
        <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Section 4 &mdash; Project Details</h3>
        
        <label class="block text-gray-300 mb-4 font-semibold text-lg">Tell us about your project</label>
        <textarea name="Project Details" rows="5" required placeholder="What are you looking to build? What problem are you trying to solve?" class="w-full bg-black/20 border border-white/10 rounded-xl p-6 text-white placeholder-gray-500 focus:outline-none focus:border-[#5E0819] focus:ring-1 focus:ring-[#5E0819] transition-all resize-none"></textarea>
      </section>

      <!-- SECTIONS 5, 6, 7: DETAILS -->
      <section class="form-section p-8 lg:p-12 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-10 -right-10 text-[#5E0819]/10 text-9xl font-black pointer-events-none">05</div>
        <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Project Logistics</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- SECTION 5 -->
          <div>
            <label class="block text-gray-300 mb-4 font-semibold">Budget</label>
            <select name="Budget" required class="form-input custom-select text-white font-medium">
              <option value="" disabled selected>Select Budget</option>
              <option value="Under ₹25,000">Under ₹25,000</option>
              <option value="₹25,000–50,000">₹25,000–50,000</option>
              <option value="₹50,000–1,00,000">₹50,000–1,00,000</option>
              <option value="₹1,00,000–3,00,000">₹1,00,000–3,00,000</option>
              <option value="₹3,00,000+">₹3,00,000+</option>
              <option value="Let's Discuss">Let's Discuss</option>
            </select>
          </div>
          <!-- SECTION 6 -->
          <div>
            <label class="block text-gray-300 mb-4 font-semibold">Timeline</label>
            <select name="Timeline" required class="form-input custom-select text-white font-medium">
              <option value="" disabled selected>Select Timeline</option>
              <option value="ASAP">ASAP</option>
              <option value="Within 2 Weeks">Within 2 Weeks</option>
              <option value="Within 1 Month">Within 1 Month</option>
              <option value="2–3 Months">2–3 Months</option>
              <option value="Flexible">Flexible</option>
            </select>
          </div>
          <!-- SECTION 7 -->
          <div>
            <label class="block text-gray-300 mb-4 font-semibold">How did you find us?</label>
            <select name="Source" required class="form-input custom-select text-white font-medium">
              <option value="" disabled selected>Select Source</option>
              <option value="Instagram">Instagram</option>
              <option value="LinkedIn">LinkedIn</option>
              <option value="Google">Google</option>
              <option value="Referral">Referral</option>
              <option value="Website">Website</option>
              <option value="YouTube">YouTube</option>
              <option value="Facebook">Facebook</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
      </section>

      <!-- SECTION 8: FINAL STEP -->
      <section class="form-section p-8 lg:p-12 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl relative overflow-hidden">
        <div class="absolute -top-10 -right-10 text-[#5E0819]/10 text-9xl font-black pointer-events-none">08</div>
        <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Section 8 &mdash; Final Step</h3>
        
        <label class="block text-gray-300 mb-6 font-semibold text-lg text-center">Preferred Contact Method</label>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
          <label class="radio-card">
            <input type="radio" name="Contact Method" value="WhatsApp" required>
            <div class="card-content flex flex-col items-center gap-2">
              <i class="fa-brands fa-whatsapp text-2xl text-green-400"></i>
              <span class="font-medium text-white">WhatsApp</span>
            </div>
          </label>
          <label class="radio-card">
            <input type="radio" name="Contact Method" value="Phone Call">
            <div class="card-content flex flex-col items-center gap-2">
              <i class="fa-solid fa-phone text-2xl text-blue-400"></i>
              <span class="font-medium text-white">Phone Call</span>
            </div>
          </label>
          <label class="radio-card">
            <input type="radio" name="Contact Method" value="Email">
            <div class="card-content flex flex-col items-center gap-2">
              <i class="fa-regular fa-envelope text-2xl text-yellow-400"></i>
              <span class="font-medium text-white">Email</span>
            </div>
          </label>
          <label class="radio-card">
            <input type="radio" name="Contact Method" value="Google Meet">
            <div class="card-content flex flex-col items-center gap-2">
              <i class="fa-solid fa-video text-2xl text-purple-400"></i>
              <span class="font-medium text-white">Google Meet</span>
            </div>
          </label>
        </div>

        <div class="mt-16 text-center">
          <button type="submit" id="submit-btn" class="relative group inline-flex items-center justify-center rounded-full bg-[#5E0819] px-12 py-5 text-xl font-bold text-white shadow-[0_20px_40px_rgba(94,8,25,0.4),inset_0_2px_4px_rgba(255,255,255,0.4)] transition-all duration-500 hover:scale-105 hover:bg-[#7b0a21] hover:shadow-[0_30px_60px_rgba(94,8,25,0.6)] active:scale-95 border-none">
            <span class="relative z-10 flex items-center gap-2">Let's Build Together 🚀</span>
            <!-- Glow effect -->
            <div class="absolute inset-0 -z-10 rounded-full bg-gradient-to-r from-[#5E0819] to-red-500 blur-xl opacity-0 transition-opacity duration-500 group-hover:opacity-60"></div>
          </button>
          <p id="form-error" class="text-red-400 mt-4 hidden">Please fill in all required fields.</p>
        </div>
      </section>
    </form>

  </div>
</main>

<script>
  // Add form submission JS right after form
  document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('project-form');
    const successScreen = document.getElementById('success-screen');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('span');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Basic styling feedback
      const originalText = btnText.innerHTML;
      btnText.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting...';
      submitBtn.style.pointerEvents = 'none';

      try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });

        if (response.ok) {
          // Success! Hide form, show success screen
          gsap.to(form, {
            opacity: 0,
            y: 50,
            duration: 0.6,
            ease: "power2.in",
            onComplete: () => {
              form.style.display = 'none';
              successScreen.style.display = 'block';
              gsap.to(successScreen, {
                opacity: 1,
                y: -30,
                duration: 0.8,
                ease: "power3.out"
              });
              
              // Scroll to top of the success screen smoothly
              window.scrollTo({
                top: document.querySelector('main').offsetTop - 100,
                behavior: 'smooth'
              });
            }
          });
        } else {
          throw new Error('Form submission failed');
        }
      } catch (error) {
        console.error(error);
        btnText.innerHTML = 'Error! Try Again.';
        setTimeout(() => {
          btnText.innerHTML = originalText;
          submitBtn.style.pointerEvents = 'auto';
        }, 3000);
      }
    });

    // Staggered reveal of form sections using GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);
    
    gsap.utils.toArray('.form-section').forEach((section, i) => {
      gsap.fromTo(section,
        { opacity: 0, y: 60, rotationX: 10, transformPerspective: 1000 },
        {
          opacity: 1,
          y: 0,
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
  });
</script>
"""

    with open(r'd:\snapticle-media\form.html', 'w', encoding='utf-8') as f:
        f.write(header + form_styles + main_content + footer + scripts)
    
    print("form.html has been successfully generated!")

if __name__ == '__main__':
    build_form()
