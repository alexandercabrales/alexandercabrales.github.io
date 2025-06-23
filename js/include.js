// js/include.js
document.addEventListener("DOMContentLoaded", () => {
  const includes = document.querySelectorAll("[data-include]");

  includes.forEach(async (el) => {
    const file = el.getAttribute("data-include");
    try {
      const res = await fetch(file);
      if (res.ok) {
        const content = await res.text();
        el.innerHTML = content;
      } else {
        el.innerHTML = `<p style="color:red;">Include failed: ${file}</p>`;
      }
    } catch (err) {
      el.innerHTML = `<p style="color:red;">Error loading ${file}</p>`;
      console.error(err);
    }
  });
});
