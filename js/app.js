// app.js - shared JavaScript for all pages
// (Currently empty - we'll add common functions here later if needed)
// app.js - shared JavaScript for all pages

document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('navToggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
    });
  }
});