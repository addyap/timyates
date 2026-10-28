// Mobile menu
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Close" : "Menu";
  });
  nav.addEventListener("click", (e) => {
    if (e.target.closest("a")) { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.textContent = "Menu"; }
  });
}
// Open the FAQ answer the URL points at
if (location.hash) {
  const el = document.querySelector(location.hash);
  if (el && el.classList.contains("faq-group")) {
    el.querySelector("details")?.setAttribute("open", "");
    requestAnimationFrame(() => el.scrollIntoView());
  }
}

// Hero: pointer tilt and scroll depth. Off when the visitor prefers reduced motion.
const hero = document.querySelector(".hero");
// Place the sun just off the arch's left edge, at any screen width
const placeSun = () => {
  const arch = hero?.querySelector(".arch-frame");
  if (!arch) return;
  const h = hero.getBoundingClientRect(), a = arch.getBoundingClientRect();
  hero.style.setProperty("--sx", (((a.left - h.left) - a.width * 0.02) / h.width * 100).toFixed(2) + "%");
};
placeSun();
addEventListener("resize", placeSun);
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (hero && !calm) {
  const frame = hero.querySelector(".arch-frame");
  if (frame && matchMedia("(hover: hover) and (pointer: fine)").matches) {
    hero.addEventListener("pointermove", (e) => {
      const r = frame.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      frame.style.setProperty("--ry", (x * 7).toFixed(2) + "deg");
      frame.style.setProperty("--rx", (-y * 5).toFixed(2) + "deg");
      frame.style.setProperty("--gx", ((x + 0.5) * 100).toFixed(1) + "%");
      frame.style.setProperty("--gy", ((y + 0.5) * 100).toFixed(1) + "%");
    });
    hero.addEventListener("pointerleave", () => {
      ["--rx", "--ry", "--gx", "--gy"].forEach((p) => frame.style.removeProperty(p));
    });
  }
  const scene = hero.querySelector(".scene");
  const sun = hero.querySelector(".sun");
  const copy = hero.querySelector(".hero-copy");
  let ticking = false;
  const update = () => {
    ticking = false;
    const y = Math.min(window.scrollY, hero.offsetHeight);
    // The scene drifts slower than the page; the sun sinks into the sea.
    if (scene) scene.style.transform = `translate3d(0, ${(y * 0.3).toFixed(1)}px, 0)`;
    if (sun) sun.style.transform = `translate3d(0, ${(y * 0.35).toFixed(1)}px, 0)`;
    if (copy) copy.style.opacity = String(Math.max(0, 1 - y / (hero.offsetHeight * 0.75)));
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
}
