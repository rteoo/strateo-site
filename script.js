const header = document.querySelector(".site-header");

const syncHeader = () => {
  if (!header) return;
  header.dataset.scrolled = String(window.scrollY > 8);
};

syncHeader();
window.addEventListener("scroll", syncHeader, { passive: true });

const menuButton = document.querySelector(".menu-toggle");
const nav = document.getElementById("navegacao-principal");

if (header && menuButton && nav) {
  const setMenu = open => {
    header.dataset.menuOpen = String(open);
    menuButton.setAttribute("aria-expanded", String(open));
  };

  menuButton.addEventListener("click", () => {
    setMenu(header.dataset.menuOpen !== "true");
  });

  nav.addEventListener("click", event => {
    if (event.target.closest("a")) setMenu(false);
  });

  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && header.dataset.menuOpen === "true") {
      setMenu(false);
      menuButton.focus();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 760 && header.dataset.menuOpen === "true") setMenu(false);
  });
}

const reveals = document.querySelectorAll(".reveal");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!reduceMotion && "IntersectionObserver" in window) {
  reveals.forEach(element => element.classList.add("is-pending"));

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove("is-pending");
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  reveals.forEach(element => observer.observe(element));
} else {
  reveals.forEach(element => element.classList.add("is-visible"));
}
