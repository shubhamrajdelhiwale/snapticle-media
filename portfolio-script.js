const header = document.querySelector(".header");
const menuBtn = document.querySelector(".menu-btn");
const closeMenu = document.querySelector(".close-menu");
const mobileMenu = document.querySelector(".mobile-menu");
const mobileLinks = document.querySelectorAll(".mobile-menu a");
const cursorGlow = document.querySelector(".cursor-glow");

window.addEventListener("scroll", () => {
  if (window.scrollY > 80) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
});

menuBtn.addEventListener("click", () => {
  mobileMenu.classList.add("active");
});

closeMenu.addEventListener("click", () => {
  mobileMenu.classList.remove("active");
});

mobileLinks.forEach((link) => {
  link.addEventListener("click", () => {
    mobileMenu.classList.remove("active");
  });
});

document.addEventListener("mousemove", (e) => {
  cursorGlow.style.left = e.clientX + "px";
  cursorGlow.style.top = e.clientY + "px";
});

const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {
  revealElements.forEach((element) => {
    const windowHeight = window.innerHeight;
    const elementTop = element.getBoundingClientRect().top;
    const revealPoint = 120;

    if (elementTop < windowHeight - revealPoint) {
      element.classList.add("active");
    }
  });
}

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);

const counters = document.querySelectorAll(".counter");
let counterStarted = false;

function startCounter() {
  const heroStats = document.querySelector(".hero-stats");

  if (!heroStats) return;

  const statsTop = heroStats.getBoundingClientRect().top;

  if (statsTop < window.innerHeight && !counterStarted) {
    counters.forEach((counter) => {
      const target = Number(counter.getAttribute("data-target"));
      let count = 0;
      const speed = target / 80;

      function updateCounter() {
        count += speed;

        if (count < target) {
          counter.innerText = Math.floor(count);
          requestAnimationFrame(updateCounter);
        } else {
          counter.innerText = target;
        }
      }

      updateCounter();
    });

    counterStarted = true;
  }
}

window.addEventListener("scroll", startCounter);
window.addEventListener("load", startCounter);

const filterButtons = document.querySelectorAll(".filter-btn");
const portfolioItems = document.querySelectorAll(".portfolio-item");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    const filterValue = button.getAttribute("data-filter");

    portfolioItems.forEach((item) => {
      const itemCategory = item.getAttribute("data-category");

      if (filterValue === "all" || filterValue === itemCategory) {
        item.style.display = "block";

        setTimeout(() => {
          item.style.opacity = "1";
          item.style.transform = "scale(1)";
        }, 100);
      } else {
        item.style.opacity = "0";
        item.style.transform = "scale(0.92)";

        setTimeout(() => {
          item.style.display = "none";
        }, 250);
      }
    });
  });
});

const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach((item) => {
  const question = item.querySelector(".faq-question");

  question.addEventListener("click", () => {
    faqItems.forEach((faq) => {
      if (faq !== item) {
        faq.classList.remove("active");
      }
    });

    item.classList.toggle("active");
  });
});

const lightbox = document.querySelector(".lightbox");
const lightboxImg = document.querySelector(".lightbox img");
const lightboxClose = document.querySelector(".lightbox-close");

portfolioItems.forEach((item) => {
  item.addEventListener("click", () => {
    const img = item.querySelector("img");

    lightbox.classList.add("active");
    lightboxImg.src = img.src;
  });
});

lightboxClose.addEventListener("click", () => {
  lightbox.classList.remove("active");
});

lightbox.addEventListener("click", (e) => {
  if (e.target === lightbox) {
    lightbox.classList.remove("active");
  }
});



const contactForm = document.querySelector(".contact-form");

if (contactForm) {
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const businessName = contactForm.elements["businessName"].value.trim();
    const name = contactForm.elements["clientName"].value.trim();
    const email = contactForm.elements["email"].value.trim();
    const phone = contactForm.elements["phone"].value.trim();
    const message = contactForm.elements["message"].value.trim();

    const whatsappNumber = "916206060595"; // apna WhatsApp number yaha daalo

    const text = `New Inquiry From Snapticle Media

Business Name: ${businessName}
Name: ${name}
Email: ${email}
Phone: ${phone}
Message: ${message}`;

    const whatsappURL = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(text)}`;

    window.open(whatsappURL, "_blank");

    contactForm.reset();
  });
}



const themeToggle = document.querySelector("#themeToggle");
const themeIcon = themeToggle ? themeToggle.querySelector("i") : null;

let savedTheme = localStorage.getItem("snapticle-theme");

if (!savedTheme) {
  savedTheme = "light";
  localStorage.setItem("snapticle-theme", "light");
}

if (savedTheme === "light") {
  document.body.classList.add("light-theme");
  if (themeIcon) themeIcon.className = "fa-solid fa-sun";
} else {
  document.body.classList.remove("light-theme");
  if (themeIcon) themeIcon.className = "fa-solid fa-moon";
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");

    if (document.body.classList.contains("light-theme")) {
      localStorage.setItem("snapticle-theme", "light");
      if (themeIcon) themeIcon.className = "fa-solid fa-sun";
    } else {
      localStorage.setItem("snapticle-theme", "dark");
      if (themeIcon) themeIcon.className = "fa-solid fa-moon";
    }
  });
}
