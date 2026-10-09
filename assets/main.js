"use strict";
document.documentElement.classList.add("js");
const toggle = document.querySelector(".menu-toggle");
const menu = document.getElementById("menu");
const narrow = matchMedia("(max-width: 850px)");
function closeMenu() { menu.hidden = narrow.matches; toggle.setAttribute("aria-expanded", "false"); }
closeMenu();
narrow.addEventListener("change", closeMenu);
toggle.addEventListener("click", () => { const expanded = toggle.getAttribute("aria-expanded") === "true"; menu.hidden = expanded; toggle.setAttribute("aria-expanded", String(!expanded)); });
menu.addEventListener("click", event => { if(event.target.closest("a")) closeMenu(); });
document.addEventListener("keydown", event => { if(event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {closeMenu();toggle.focus();} });
document.getElementById("year").textContent = new Date().getFullYear();
