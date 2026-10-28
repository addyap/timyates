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
