const header = document.querySelector(".site-header");

const syncHeader = () => {
  if (!header) return;
  header.dataset.scrolled = String(window.scrollY > 8);
};

syncHeader();
window.addEventListener("scroll", syncHeader, { passive: true });

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
