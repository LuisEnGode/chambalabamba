document.addEventListener("DOMContentLoaded", function () {
  const video = document.getElementById("chambaVideo");
  const playBtn = document.getElementById("playBtn");

  if (video && playBtn) {
    playBtn.addEventListener("click", function (e) {
      e.preventDefault();

      if (video.paused) {
        video.play();
        playBtn.style.display = "none"; // Oculta el botón después de reproducir
      } else {
        video.pause();
        playBtn.style.display = "block"; // Vuelve a mostrar si se pausa
      }
    });
  }
});
