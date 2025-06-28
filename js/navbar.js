// js/navbar.js
document.addEventListener("DOMContentLoaded", () => {
  const waitForNavbar = setInterval(() => {
    const toggleButton = document.getElementById("menu-toggle");
    const navLinks = document.getElementById("nav-links");

    if (toggleButton && navLinks) {
      // ✅ Found the elements; set up event
      toggleButton.addEventListener("click", () => {
        navLinks.classList.toggle("show");
      });

      // ✅ Set active link
      const links = navLinks.querySelectorAll("a");
      links.forEach((link) => {
        if (link.href === window.location.href) {
          link.classList.add("active");
        }
      });

      clearInterval(waitForNavbar); // Stop checking
    }
  }, 100); // Check every 100ms
});