document.addEventListener("DOMContentLoaded", function () {
  const toggles = document.querySelectorAll(".toggle-note");
  toggles.forEach(toggle => {
    toggle.addEventListener("click", () => {
      const body = toggle.nextElementSibling;
      if (body.classList.contains("show")) {
        body.classList.remove("show");
      } else {
        body.classList.add("show");
      }
    });
  });
});


function toggleCard(card) {
    card.classList.toggle('expanded');
    const details = card.querySelector('.card-details');
    if (card.classList.contains('expanded')) {
      details.classList.remove('d-none');
    } else {
      details.classList.add('d-none');
    }
  }