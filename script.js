const topbar = document.querySelector("[data-topbar]");
const navLinks = Array.from(document.querySelectorAll("[data-nav-link]"));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const syncTopbar = () => {
  if (!topbar) {
    return;
  }
  topbar.classList.toggle("is-scrolled", window.scrollY > 12);
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        return;
      }

      navLinks.forEach((link) => {
        const isActive = link.getAttribute("href") === `#${entry.target.id}`;
        if (isActive) {
          link.setAttribute("aria-current", "true");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    });
  },
  {
    rootMargin: "-35% 0px -50% 0px",
    threshold: 0.05
  }
);

sections.forEach((section) => observer.observe(section));
syncTopbar();
window.addEventListener("scroll", syncTopbar, { passive: true });

