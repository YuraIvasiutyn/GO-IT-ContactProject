(() => {
    const getPreferredTheme = () => 
        window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

    const setTheme = theme => 
        document.documentElement.setAttribute('data-bs-theme', theme);

    setTheme(getPreferredTheme());

    window.matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', e => setTheme(e.matches ? 'dark' : 'light'));
})();

function applyTheme(theme) {
    if (theme === "auto") {
      document.documentElement.removeAttribute("data-bs-theme");
    } else {
      document.documentElement.setAttribute("data-bs-theme", theme);
    }
  }

function changeTheme(theme) {
    localStorage.setItem("theme", theme);
    applyTheme(theme);
}

document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("theme") || "auto";
    document.getElementById("theme-select").value = savedTheme;
    applyTheme(savedTheme);
  });