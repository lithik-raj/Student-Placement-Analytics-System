document.addEventListener("DOMContentLoaded", function () {
  // Back button
  const backButtons = document.querySelectorAll(".back-button");

  backButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      window.history.back();
    });
  });

  // Page loading effect
  document.body.classList.add("page-loaded");
});
