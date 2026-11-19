document.addEventListener("DOMContentLoaded", function () {
  // Back button functionality
  const backButtons = document.querySelectorAll(".back-button");
  backButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      window.history.back();
    });
  });

  // Real-time Student Search
  const searchInput = document.getElementById("studentSearch");
  const studentsGrid = document.getElementById("studentsGrid");

  if (searchInput && studentsGrid) {
    const studentCards = studentsGrid.querySelectorAll(".student-card");

    searchInput.addEventListener("input", function () {
      const filter = this.value.toLowerCase().trim();
      let matchCount = 0;

      studentCards.forEach(function (card) {
        const text = card.textContent.toLowerCase();
        if (text.includes(filter)) {
          card.style.display = "";
          matchCount++;
        } else {
          card.style.display = "none";
        }
      });

      // Show/hide 'no results' message
      let noResultMsg = document.getElementById("noSearchResult");
      if (matchCount === 0 && studentCards.length > 0) {
        if (!noResultMsg) {
          noResultMsg = document.createElement("div");
          noResultMsg.id = "noSearchResult";
          noResultMsg.className = "empty-state";
          noResultMsg.textContent = "No students match your search.";
          studentsGrid.appendChild(noResultMsg);
        }
        noResultMsg.style.display = "block";
      } else if (noResultMsg) {
        noResultMsg.style.display = "none";
      }
    });
  }

  // Page loaded class
  document.body.classList.add("page-loaded");
});
