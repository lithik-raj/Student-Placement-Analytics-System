// =========================================================
// PLACEMENT ANALYTICS SYSTEM - ENTERPRISE DASHBOARD SCRIPT
// Managing 1,200 Student Profiles with Chart.js & Instant Search
// =========================================================

document.addEventListener("DOMContentLoaded", function () {
  // 1. Initialize Chart.js Dashboard Charts
  initDashboardCharts();

  // 2. Initialize 1,200 Student Paginated Directory & Filters
  initStudentDirectory();
});

// =========================================================
// 1. CHART.JS INITIALIZATION
// =========================================================

function initDashboardCharts() {
  const chartDataEl = document.getElementById("chartDataScript");
  if (!chartDataEl) return;

  let data = {};
  try {
    data = JSON.parse(chartDataEl.textContent);
  } catch (e) {
    console.error("Failed to parse chart data JSON:", e);
    return;
  }

  // Set global Chart.js defaults for dark cyberpunk theme
  Chart.defaults.color = "#a8b3c7";
  Chart.defaults.font.family = "Inter, 'Segoe UI', Arial, sans-serif";
  Chart.defaults.plugins.tooltip.backgroundColor = "rgba(10, 16, 32, 0.95)";
  Chart.defaults.plugins.tooltip.titleColor = "#00f7ff";
  Chart.defaults.plugins.tooltip.bodyColor = "#f4f7ff";
  Chart.defaults.plugins.tooltip.borderColor = "rgba(0, 229, 255, 0.3)";
  Chart.defaults.plugins.tooltip.borderWidth = 1;
  Chart.defaults.plugins.tooltip.padding = 10;
  Chart.defaults.plugins.tooltip.cornerRadius = 8;

  // Chart 1: Department Placement Performance (Grouped Bar Chart)
  const ctxDept = document.getElementById("deptChart");
  if (ctxDept) {
    // Shorten department labels for clean mobile layout
    const shortLabels = (data.dept_labels || []).map(d => {
      if (d.includes("Artificial Intelligence")) return "AI & DS";
      if (d.includes("Computer Science")) return "CSE";
      if (d.includes("Information Technology")) return "IT";
      if (d.includes("Electronics")) return "ECE";
      if (d.includes("Electrical")) return "EEE";
      if (d.includes("Mechanical")) return "MECH";
      return d;
    });

    new Chart(ctxDept, {
      type: "bar",
      data: {
        labels: shortLabels,
        datasets: [
          {
            label: "Total Students",
            data: data.dept_totals || [],
            backgroundColor: "rgba(0, 229, 255, 0.35)",
            borderColor: "#00e5ff",
            borderWidth: 1.5,
            borderRadius: 6
          },
          {
            label: "Placed Students",
            data: data.dept_placed || [],
            backgroundColor: "rgba(0, 255, 157, 0.45)",
            borderColor: "#00ff9d",
            borderWidth: 1.5,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { boxWidth: 14, font: { size: 12 } } }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.05)" } },
          y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, beginAtZero: true }
        }
      }
    });
  }

  // Chart 2: Overall Placement Ratio (Doughnut Chart)
  const ctxRatio = document.getElementById("placementRatioChart");
  if (ctxRatio) {
    new Chart(ctxRatio, {
      type: "doughnut",
      data: {
        labels: data.status_labels || ["Placed", "Not Placed"],
        datasets: [
          {
            data: data.status_counts || [834, 366],
            backgroundColor: ["#00ff9d", "#ff4d6d"],
            borderColor: "#0d1528",
            borderWidth: 3,
            hoverOffset: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "68%",
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 14, font: { size: 12 } } }
        }
      }
    });
  }

  // Chart 3: Salary Package Tiers (Polar/Bar Chart)
  const ctxTier = document.getElementById("salaryTierChart");
  if (ctxTier) {
    new Chart(ctxTier, {
      type: "bar",
      data: {
        labels: data.tier_labels || ["Super Dream", "Dream", "Regular", "Mass"],
        datasets: [
          {
            label: "Offers Count",
            data: data.tier_counts || [],
            backgroundColor: [
              "rgba(255, 209, 102, 0.6)",
              "rgba(155, 92, 255, 0.6)",
              "rgba(0, 229, 255, 0.6)",
              "rgba(111, 124, 148, 0.6)"
            ],
            borderColor: ["#ffd166", "#9b5cff", "#00e5ff", "#a8b3c7"],
            borderWidth: 1.5,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, beginAtZero: true }
        }
      }
    });
  }

  // Chart 4: Top Recruiting Partners (Horizontal Bar Chart)
  const ctxComp = document.getElementById("companyChart");
  if (ctxComp) {
    new Chart(ctxComp, {
      type: "bar",
      data: {
        labels: data.company_labels || [],
        datasets: [
          {
            label: "Students Recruited",
            data: data.company_hires || [],
            backgroundColor: "rgba(0, 247, 255, 0.35)",
            borderColor: "#00f7ff",
            borderWidth: 1.5,
            borderRadius: 6
          }
        ]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, beginAtZero: true },
          y: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 5: Academic CGPA Distribution (Area Chart)
  const ctxCgpa = document.getElementById("cgpaChart");
  if (ctxCgpa) {
    new Chart(ctxCgpa, {
      type: "line",
      data: {
        labels: data.cgpa_dist_labels || [],
        datasets: [
          {
            label: "Students",
            data: data.cgpa_dist_counts || [],
            backgroundColor: "rgba(0, 229, 255, 0.15)",
            borderColor: "#00e5ff",
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointBackgroundColor: "#00f7ff",
            pointBorderColor: "#fff",
            pointRadius: 5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, beginAtZero: true }
        }
      }
    });
  }

  // Chart 6: High-Demand Technical Skills (Radar Chart)
  const ctxSkills = document.getElementById("skillsRadarChart");
  if (ctxSkills) {
    new Chart(ctxSkills, {
      type: "radar",
      data: {
        labels: (data.skill_labels || []).slice(0, 8),
        datasets: [
          {
            label: "Proficient Students",
            data: (data.skill_counts || []).slice(0, 8),
            backgroundColor: "rgba(155, 92, 255, 0.25)",
            borderColor: "#9b5cff",
            borderWidth: 2,
            pointBackgroundColor: "#00e5ff",
            pointBorderColor: "#fff",
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: "rgba(255, 255, 255, 0.1)" },
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            pointLabels: { color: "#a8b3c7", font: { size: 11 } },
            ticks: { display: false }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }
}

// =========================================================
// 2. 1,200 STUDENT PROFILES DIRECTORY (FAST FILTER & PAGINATION)
// =========================================================

function initStudentDirectory() {
  const searchInput = document.getElementById("studentSearchInput");
  const deptFilter = document.getElementById("deptFilter");
  const statusFilter = document.getElementById("statusFilter");
  const readinessFilter = document.getElementById("readinessFilter");
  const sortOrder = document.getElementById("sortOrder");
  const gridContainer = document.getElementById("studentsGridContainer");
  const resultsCount = document.getElementById("resultsCount");
  const totalCount = document.getElementById("totalCount");
  const pageSummary = document.getElementById("pageSummary");

  const firstBtn = document.getElementById("firstPageBtn");
  const prevBtn = document.getElementById("prevPageBtn");
  const nextBtn = document.getElementById("nextPageBtn");
  const lastBtn = document.getElementById("lastPageBtn");

  if (!gridContainer) return;

  let currentPage = 1;
  const pageSize = 24;
  let totalPages = 50;
  let searchTimeout = null;

  async function fetchStudents(page = 1) {
    currentPage = page;

    const queryParams = new URLSearchParams({
      page: currentPage,
      limit: pageSize,
      search: searchInput ? searchInput.value.trim() : "",
      department: deptFilter ? deptFilter.value : "ALL",
      status: statusFilter ? statusFilter.value : "ALL",
      readiness: readinessFilter ? readinessFilter.value : "ALL",
      sort: sortOrder ? sortOrder.value : "id_asc"
    });

    try {
      // Optional subtle opacity transition
      gridContainer.style.opacity = "0.5";

      const res = await fetch(`/api/students?${queryParams.toString()}`);
      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
      const result = await res.json();

      renderStudents(result.students);

      totalPages = result.total_pages || 1;
      const count = result.students.length;
      const total = result.total;

      if (resultsCount) resultsCount.textContent = count;
      if (totalCount) totalCount.textContent = total;
      if (pageSummary) pageSummary.textContent = `Page ${currentPage} of ${totalPages}`;

      // Update button states
      if (firstBtn) firstBtn.disabled = (currentPage <= 1);
      if (prevBtn) prevBtn.disabled = (currentPage <= 1);
      if (nextBtn) nextBtn.disabled = (currentPage >= totalPages);
      if (lastBtn) lastBtn.disabled = (currentPage >= totalPages);

    } catch (err) {
      console.error("Error loading students:", err);
    } finally {
      gridContainer.style.opacity = "1";
    }
  }

  function renderStudents(students) {
    if (!students || students.length === 0) {
      gridContainer.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1; padding: 40px; text-align: center;">
          <h3 style="color: var(--cyan); margin-bottom: 8px;">No Students Found</h3>
          <p style="color: var(--text-muted);">Try adjusting your search criteria or resetting filters.</p>
        </div>
      `;
      return;
    }

    const html = students.map(s => {
      const initial = (s.name || "S")[0].toUpperCase();
      const shortDept = (s.department || "").split(" & ")[0];
      const isPlaced = (s.placement_status === "PLACED");

      const statusBadge = isPlaced
        ? `<span class="badge-status-placed">✓ ${escapeHtml(s.company_name || "Placed")} (${s.package_lpa || ""} LPA)</span>`
        : `<span class="badge-status-unplaced">Not Placed</span>`;

      return `
        <a href="/student/${s.student_id}" class="student-card-enhanced">
          <div class="student-card-top">
            <div class="student-avatar">${initial}</div>
            <div class="student-meta">
              <div class="student-name-text">${escapeHtml(s.name)}</div>
              <div class="student-id-text">ID: #${s.student_id} • ${escapeHtml(s.year || "4th Year")}</div>
            </div>
          </div>

          <div class="student-badges-row">
            <span class="badge-dept">${escapeHtml(shortDept)}</span>
            <span class="badge-cgpa">CGPA: ${s.cgpa}</span>
            ${statusBadge}
          </div>

          <div class="student-readiness-meter">
            <div class="readiness-meter-labels">
              <span>${escapeHtml(s.readiness_status || "Developing")}</span>
              <span><strong>${s.readiness_score || 0}%</strong></span>
            </div>
            <div class="readiness-track">
              <div class="readiness-fill" style="width: ${s.readiness_score || 0}%;"></div>
            </div>
          </div>
        </a>
      `;
    }).join("");

    gridContainer.innerHTML = html;
  }

  function escapeHtml(text) {
    if (!text) return "";
    return text.toString()
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Event Listeners with Debounce for Search
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        fetchStudents(1);
      }, 250);
    });
  }

  [deptFilter, statusFilter, readinessFilter, sortOrder].forEach(el => {
    if (el) {
      el.addEventListener("change", () => fetchStudents(1));
    }
  });

  // Pagination click handlers
  if (firstBtn) firstBtn.addEventListener("click", () => { if (currentPage > 1) fetchStudents(1); });
  if (prevBtn) prevBtn.addEventListener("click", () => { if (currentPage > 1) fetchStudents(currentPage - 1); });
  if (nextBtn) nextBtn.addEventListener("click", () => { if (currentPage < totalPages) fetchStudents(currentPage + 1); });
  if (lastBtn) lastBtn.addEventListener("click", () => { if (currentPage < totalPages) fetchStudents(totalPages); });
}
