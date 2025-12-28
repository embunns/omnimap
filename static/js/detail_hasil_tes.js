/* =============================================
   DETAIL HASIL TES - JAVASCRIPT
   File: detail_hasil_tes.js
   ============================================= */

/* =============== INITIALIZATION =============== */
document.addEventListener("DOMContentLoaded", () => {
  console.log("Detail Hasil Tes page loaded");

  // Initialize sidebar toggle
  initSidebarToggle();

  // Initialize page features
  initializeBackButton();
  initializeTooltips();
  animateTableRows();

  // Setup event listeners
  setupEventListeners();
});

/* =============== SIDEBAR TOGGLE =============== */
function initSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const toggleButtons = document.querySelectorAll(".toggle-sidebar");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.stopPropagation(); // Prevent event from bubbling
      // Deteksi apakah sedang dalam mode mobile atau desktop
      const isMobile = window.innerWidth <= 768;

      if (isMobile) {
        // Di mobile: toggle class 'mobile-active'
        sidebar.classList.toggle("mobile-active");
        if (sidebarOverlay) {
          sidebarOverlay.classList.toggle("active");
        }
      } else {
        // Di desktop: toggle class 'hide'
        sidebar.classList.toggle("hide");
        if (content) {
          content.classList.toggle("full-width");
        }
      }
    });
  });

  // Close sidebar when clicking overlay
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", function () {
      sidebar.classList.remove("mobile-active");
      sidebarOverlay.classList.remove("active");
    });
  }

  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", function (e) {
    const isMobile = window.innerWidth <= 768;
    if (
      isMobile &&
      sidebar.classList.contains("mobile-active") &&
      !sidebar.contains(e.target) &&
      !e.target.classList.contains("toggle-sidebar")
    ) {
      sidebar.classList.remove("mobile-active");
      if (sidebarOverlay) {
        sidebarOverlay.classList.remove("active");
      }
    }
  });

  // Prevent clicks inside sidebar from closing it
  if (sidebar) {
    sidebar.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  }
}

/* =============== SETUP EVENT LISTENERS =============== */
function setupEventListeners() {
  // Logout functionality
  const signOutBtn = document.getElementById("signOutBtn");
  const logoutModal = document.getElementById("logoutModal");
  const logoutCancel = document.getElementById("logoutCancel");
  const logoutConfirm = document.getElementById("logoutConfirm");

  if (signOutBtn && logoutModal) {
    signOutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      logoutModal.classList.add("active");
    });
  }

  if (logoutCancel && logoutModal) {
    logoutCancel.addEventListener("click", function () {
      logoutModal.classList.remove("active");
    });
  }

  if (logoutConfirm) {
    logoutConfirm.addEventListener("click", function () {
      fetch("/api/logout", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
          console.log("Logout response:", data);
          if (data.success) {
            window.location.href = "/login";
          }
        })
        .catch((error) => {
          console.error("Logout error:", error);
          // Still redirect to login even on error
          window.location.href = "/login";
        });
    });
  }

  // Close modal when clicking outside
  if (logoutModal) {
    logoutModal.addEventListener("click", function (e) {
      if (e.target === logoutModal) {
        logoutModal.classList.remove("active");
      }
    });
  }
}

/* =======================
   BACK BUTTON HANDLER
======================== */
function initializeBackButton() {
  const backBtn = document.querySelector(".btn-back");

  if (backBtn) {
    backBtn.addEventListener("click", (e) => {
      e.preventDefault();

      // Add smooth fade transition
      document.body.style.transition = "opacity 0.3s ease";
      document.body.style.opacity = "0.7";

      setTimeout(() => {
        window.location.href = backBtn.getAttribute("href");
      }, 300);
    });
  }
}

/* =======================
   INITIALIZE TOOLTIPS
======================== */
function initializeTooltips() {
  // Initialize Bootstrap tooltips if they exist
  const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );

  if (tooltipTriggerList.length > 0 && typeof bootstrap !== "undefined") {
    [...tooltipTriggerList].map(
      (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
    );
  }
}

/* =======================
   ANIMATE TABLE ROWS
======================== */
function animateTableRows() {
  const tables = document.querySelectorAll(".dimension-table");

  tables.forEach((table) => {
    const rows = table.querySelectorAll("tbody tr");

    // Add staggered fade-in animation to each row
    rows.forEach((row, index) => {
      row.style.opacity = "0";
      row.style.transform = "translateY(10px)";
      row.style.transition = "opacity 0.3s ease, transform 0.3s ease";

      setTimeout(() => {
        row.style.opacity = "1";
        row.style.transform = "translateY(0)";
      }, 50 * index);
    });
  });
}

/* =======================
   TABLE SEARCH/FILTER (OPTIONAL)
======================== */
function initializeTableSearch() {
  // Create search input if needed
  const detailCards = document.querySelectorAll(".detail-card");

  detailCards.forEach((card) => {
    const table = card.querySelector(".dimension-table");

    if (table) {
      // Create search input
      const searchDiv = document.createElement("div");
      searchDiv.className = "mb-3";
      searchDiv.innerHTML = `
                <input type="text" 
                       class="form-control table-search" 
                       placeholder="Cari konstruk...">
            `;

      // Insert before table
      table.parentElement.insertBefore(
        searchDiv,
        table.parentElement.firstChild
      );

      // Add search functionality
      const searchInput = searchDiv.querySelector(".table-search");
      searchInput.addEventListener("input", (e) => {
        filterTable(e.target.value, table);
      });
    }
  });
}

/* =======================
   FILTER TABLE FUNCTION
======================== */
function filterTable(searchTerm, table) {
  const rows = table.querySelectorAll("tbody tr");
  const lowerSearchTerm = searchTerm.toLowerCase();

  rows.forEach((row) => {
    const constructName = row.querySelector(".construct-column");

    if (constructName) {
      const text = constructName.textContent.toLowerCase();

      if (text.includes(lowerSearchTerm)) {
        row.style.display = "";
        row.style.opacity = "1";
      } else {
        row.style.display = "none";
      }
    }
  });
}

/* =======================
   EXPORT TABLE TO CSV (OPTIONAL)
======================== */
function exportTableToCSV(tableElement, filename) {
  if (!tableElement) {
    console.error("Table element not found");
    return;
  }

  let csv = [];
  const rows = tableElement.querySelectorAll("tr");

  rows.forEach((row) => {
    const cols = row.querySelectorAll("td, th");
    const rowData = [];

    cols.forEach((col) => {
      // Get text content, remove extra spaces
      let text = col.innerText.trim();
      // Escape quotes
      text = text.replace(/"/g, '""');
      // Wrap in quotes if contains comma
      if (text.includes(",")) {
        text = `"${text}"`;
      }
      rowData.push(text);
    });

    csv.push(rowData.join(","));
  });

  // Create and download CSV
  downloadCSV(csv.join("\n"), filename);
}

/* =======================
   DOWNLOAD CSV HELPER
======================== */
function downloadCSV(csvContent, filename) {
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");

  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

/* =======================
   PRINT PAGE FUNCTION
======================== */
function printDetailPage() {
  window.print();
}

/* =======================
   HIGHLIGHT CATEGORY
======================== */
function highlightCategory(category) {
  const badges = document.querySelectorAll(".kategori-badge");

  // Remove all highlights
  badges.forEach((badge) => {
    badge.style.transform = "scale(1)";
    badge.style.boxShadow = "none";
  });

  // Highlight matching category
  if (category) {
    badges.forEach((badge) => {
      if (
        badge.classList.contains(
          `kategori-${category.toLowerCase().replace(" ", "-")}`
        )
      ) {
        badge.style.transform = "scale(1.1)";
        badge.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
        badge.style.transition = "all 0.3s ease";
      }
    });
  }
}

/* =======================
   SCROLL TO SECTION
======================== */
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);

  if (section) {
    section.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
}

/* =======================
   EXPORT FUNCTIONS TO GLOBAL SCOPE
======================== */
if (typeof window !== "undefined") {
  window.exportTableToCSV = exportTableToCSV;
  window.filterTable = filterTable;
  window.printDetailPage = printDetailPage;
  window.highlightCategory = highlightCategory;
  window.scrollToSection = scrollToSection;
}

/* =======================
   ADD EXPORT BUTTONS (OPTIONAL)
======================== */
function addExportButtons() {
  const detailCards = document.querySelectorAll(".detail-card");

  detailCards.forEach((card) => {
    const table = card.querySelector(".dimension-table");
    const sectionTitle = card.querySelector(".section-title");

    if (table && sectionTitle) {
      // Create export button
      const exportBtn = document.createElement("button");
      exportBtn.className = "btn btn-sm btn-outline-secondary float-end";
      exportBtn.innerHTML = '<i class="bi bi-download me-1"></i>Export CSV';

      exportBtn.addEventListener("click", () => {
        const filename =
          sectionTitle.textContent
            .trim()
            .replace(/[^a-z0-9]/gi, "_")
            .toLowerCase() + ".csv";
        exportTableToCSV(table, filename);
      });

      sectionTitle.appendChild(exportBtn);
    }
  });
}

// Uncomment to enable export buttons
// setTimeout(addExportButtons, 500);
