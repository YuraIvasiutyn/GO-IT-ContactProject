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


  function raiseCardZIndex(noteId) {
  document.querySelectorAll('.note-card').forEach(el => el.style.zIndex = 1);
  const card = document.getElementById(`note-card-${noteId}`);
  if (card) {
    card.style.zIndex = 1055; // вище за dropdown-menu
  }
}
/*
function raiseCardZIndex(noteId) {
  document.querySelectorAll('.note-card').forEach(el => {
    el.style.zIndex = ''; // скинь z-index повністю
  });

  const card = document.getElementById(`note-card-${noteId}`);
  if (card) {
    card.style.zIndex = '1055'; // підніми лише одну
  }

  // І додатково: "притисни" всі сусідні .dropdown-menu
  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.style.zIndex = '1060';
  });
}
*/
function resetCardZIndex(noteId) {
  const card = document.getElementById(`note-card-${noteId}`);
  if (card) {
    card.style.zIndex = 1;
  }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.toggle-collapse').forEach(function (el) {
      el.addEventListener('click', function () {
        const targetId = el.getAttribute('data-target');
        const target = document.querySelector(targetId);
        if (target) {
          target.classList.toggle('show');
        }
      });
    });
  });


function selectColor(hex) {
    document.getElementById('note-color').value = hex;

    // (опціонально) підсвітка вибраного кольору
    document.querySelectorAll('[onclick^="selectColor"]').forEach(btn => {
      btn.style.outline = "";
    });
    const activeBtn = [...document.querySelectorAll('[onclick^="selectColor"]')]
      .find(btn => btn.style.backgroundColor.toLowerCase() === hex.toLowerCase());
    if (activeBtn) {
      activeBtn.style.outline = "3px solid black";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const colorInput = document.getElementById('note-color');
    const buttons = document.querySelectorAll('.color-btn');

    function getTheme() {
      return document.documentElement.getAttribute('data-bs-theme') || 'light';
    }

    function highlightSelectedColor() {
      const theme = getTheme();

      buttons.forEach(btn => {
        const btnColor = btn.getAttribute('data-color');
        btn.classList.remove('selected-light', 'selected-dark');

        if (btnColor.toLowerCase() === colorInput.value.toLowerCase()) {
          btn.classList.add(theme === 'dark' ? 'selected-dark' : 'selected-light');
        }
      });
    }

    highlightSelectedColor();

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const selectedColor = btn.getAttribute('data-color');
        colorInput.value = selectedColor;
        highlightSelectedColor();
      });
    });

    // Додатково: оновлювати підсвітку при зміні теми (опціонально, якщо є перемикач)
    const themeSelect = document.getElementById('theme-select');
    if (themeSelect) {
      themeSelect.addEventListener('change', () => {
        setTimeout(highlightSelectedColor, 100);
      });
    }
  });