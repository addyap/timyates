// Site behaviour and motion. Spec: docs/MOTION.md
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;

// One rAF-throttled scroll loop shared by everything that follows scroll
const onScroll = [];
let ticking = false;
const runScroll = () => { ticking = false; onScroll.forEach((fn) => fn(window.scrollY)); };
addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(runScroll); } }, { passive: true });
addEventListener("resize", () => requestAnimationFrame(runScroll));

// Mobile menu
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("nav");
if (toggle && nav) {
  const setOpen = (open) => {
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Close" : "Menu";
    if (typeof updateHeader === "function") updateHeader();
  };
  toggle.addEventListener("click", () => setOpen(!nav.classList.contains("open")));
  nav.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
  addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("open")) { setOpen(false); toggle.focus(); } });
}

// Header: floats over a dark opening, turns solid past it (or while the menu is open)
const header = document.querySelector(".site-header");
const opening = document.body.classList.contains("dark-top") ? document.querySelector("main > :first-child") : null;
const updateHeader = (y = window.scrollY) => {
  if (!header) return;
  header.classList.toggle("is-scrolled", y > 8);
  if (opening) header.classList.toggle("is-solid", !!nav?.classList.contains("open") || y > opening.offsetHeight - 80);
};
onScroll.push(updateHeader);

// Scroll reveals: each element once, then forgotten
const reveals = document.querySelectorAll("[data-reveal]");
reveals.forEach((el) => {
  if (el.dataset.reveal === "head" || el.dataset.reveal === "stagger") {
    [...el.children].forEach((child, i) => child.style.setProperty("--i", Math.min(i, 6)));
  }
});
const show = (el) => el.classList.add("is-in");
if (calm || !("IntersectionObserver" in window)) {
  reveals.forEach(show);
} else {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { show(entry.target); io.unobserve(entry.target); }
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
  reveals.forEach((el) => io.observe(el));
}

// "How it works": the progress line fills and steps light up as they pass 60% of the screen
const steps = document.querySelector("[data-steps]");
if (steps && !calm) {
  const items = [...steps.children];
  // The line runs from the first marker to the last one
  let tail = 0;
  const measure = () => { tail = items[items.length - 1].offsetHeight - 16; steps.style.setProperty("--tail", tail + "px"); };
  measure();
  addEventListener("resize", measure);
  onScroll.push(() => {
    const mark = innerHeight * 0.6, r = steps.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, (mark - r.top - 16) / (r.height - 16 - tail)));
    steps.style.setProperty("--p", p.toFixed(3));
    items.forEach((li) => li.classList.toggle("is-active", li.getBoundingClientRect().top < mark));
  });
}

// Article reading progress
const bar = document.querySelector(".read-progress");
const prose = document.querySelector(".article .prose");
if (bar && prose) {
  onScroll.push(() => {
    const r = prose.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, (innerHeight * 0.5 - r.top) / r.height));
    bar.style.setProperty("--read", p.toFixed(3));
  });
}

// FAQ: open the group a link points at
if (location.hash) {
  const el = document.querySelector(location.hash);
  if (el && el.classList.contains("faq-group")) {
    show(el);
    el.querySelector("details")?.setAttribute("open", "");
    requestAnimationFrame(() => el.scrollIntoView());
  }
}

// Hero
const hero = document.querySelector(".hero");
if (hero) {
  // Place the sun just off the arch's left edge, at any screen width
  const placeSun = () => {
    const arch = hero.querySelector(".arch-frame");
    if (!arch) return;
    const h = hero.getBoundingClientRect(), a = arch.getBoundingClientRect();
    hero.style.setProperty("--sx", (((a.left - h.left) - a.width * 0.02) / h.width * 100).toFixed(2) + "%");
  };
  placeSun();
  addEventListener("resize", placeSun);

  if (!calm) {
    // Arch tilts towards the pointer; warm light follows it. Fine pointers only.
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
    // Scene drifts slower than the page; the sun sinks into the sea; copy fades.
    const scene = hero.querySelector(".scene");
    const sun = hero.querySelector(".sun");
    const copy = hero.querySelector(".hero-copy");
    onScroll.push((sy) => {
      const y = Math.min(sy, hero.offsetHeight);
      if (scene) scene.style.transform = `translate3d(0, ${(y * 0.3).toFixed(1)}px, 0)`;
      if (sun) sun.style.transform = `translate3d(0, ${(y * 0.35).toFixed(1)}px, 0)`;
      if (copy) copy.style.opacity = String(Math.max(0, 1 - y / (hero.offsetHeight * 0.75)));
    });
  }
}

runScroll();
