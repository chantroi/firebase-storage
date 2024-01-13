const player = new Plyr('#player');
function toggleDarkMode() {
      const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.body.classList.toggle('dark-mode', isDarkMode);
    }
    window.addEventListener('load', toggleDarkMode);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', toggleDarkMode);