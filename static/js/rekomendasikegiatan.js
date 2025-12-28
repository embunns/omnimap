/* =====================================================
   REKOMENDASI KEGIATAN - JAVASCRIPT
   File ini berisi semua JavaScript untuk halaman rekomendasi kegiatan
   ===================================================== */

let allActivities = [];
let filteredActivities = [];
let currentFilter = "semua";
let searchQuery = "";
let categoryCounts = {};

// =============== INITIALIZATION ===============
document.addEventListener("DOMContentLoaded", function () {
  // Initialize sidebar toggle
  initSidebarToggle();

  // Load activities
  loadActivities();

  // Setup event listeners
  setupEventListeners();

  // Setup filter and search
  setupFilterAndSearch();
});

// =============== SIDEBAR TOGGLE ===============
function initSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");
  const toggleButtons = document.querySelectorAll(".toggle-sidebar");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Deteksi apakah sedang dalam mode mobile atau desktop
      const isMobile = window.innerWidth <= 768;

      if (isMobile) {
        // Di mobile: toggle class 'mobile-active'
        sidebar.classList.toggle("mobile-active");
      } else {
        // Di desktop: toggle class 'hide'
        sidebar.classList.toggle("hide");
        content.classList.toggle("full-width");
      }
    });
  });
}

// =============== LOAD ACTIVITIES ===============
async function loadActivities() {
  try {
    const response = await fetch("/api/recommended-activities");
    const data = await response.json();

    if (data.error) {
      showError(data.error);
      return;
    }

    allActivities = data.activities;
    categoryCounts = data.category_counts;
    filteredActivities = [...allActivities];

    renderCategories();
    renderActivities();
  } catch (error) {
    console.error("Error loading activities:", error);
    showError("Gagal memuat data kegiatan");
  }
}

// =============== RENDER CATEGORIES ===============
function renderCategories() {
  const categoryGrid = document.getElementById("categoryGrid");

  const categories = [
    {
      name: "UKM",
      slug: "ukm",
      icon: "M12 20v-10M18 20V4M6 20v-4",
      count: categoryCounts.ukm || 0,
    },
    {
      name: "Kepanitiaan",
      slug: "kepanitiaan",
      icon: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z M14 2v6h6 M12 18v-6 M9 15h6",
      count: categoryCounts.kepanitiaan || 0,
    },
    {
      name: "Organisasi",
      slug: "organisasi",
      icon: "M20 6L9 17l-5-5",
      count: categoryCounts.organisasi || 0,
    },
    {
      name: "Lomba",
      slug: "lomba",
      icon: "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2 M9 7a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M23 21v-2a4 4 0 0 0-3-3.87 M16 3.13a4 4 0 0 1 0 7.75",
      count: categoryCounts.lomba || 0,
    },
  ];

  categoryGrid.innerHTML = categories
    .map(
      (cat) => `
        <div class="category-card ${cat.slug}" data-category="${cat.slug}">
            <div class="category-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="${cat.icon}"/>
                </svg>
            </div>
            <div class="category-count">${cat.count}</div>
            <div class="category-name">${cat.name}</div>
        </div>
    `
    )
    .join("");

  // Add click handlers
  document.querySelectorAll(".category-card").forEach((card) => {
    card.addEventListener("click", function () {
      const category = this.getAttribute("data-category");
      currentFilter = category;

      document.querySelectorAll(".filter-pill").forEach((pill) => {
        pill.classList.remove("active");
        if (pill.getAttribute("data-filter") === category) {
          pill.classList.add("active");
        }
      });

      filterActivities();
      document
        .querySelector(".recommendations-header")
        .scrollIntoView({ behavior: "smooth" });
    });
  });
}

// =============== RENDER ACTIVITIES ===============
function renderActivities() {
  const container = document.getElementById("activitiesList");

  if (filteredActivities.length === 0) {
    container.innerHTML = `
        <div class="no-results">
            <div class="no-results-icon">🔍</div>
            <h3>Tidak ada kegiatan ditemukan</h3>
            <p>Coba ubah filter atau kata kunci pencarian</p>
        </div>
    `;
    return;
  }

  container.innerHTML = filteredActivities
    .map((activity) => {
      const [current, max] = activity.peserta
        .split("/")
        .map((n) => parseInt(n));
      const progressPercent = (current / max) * 100;

      let matchBadgeClass = "badge-match";
      if (activity.match_percentage < 60) matchBadgeClass += " low";
      else if (activity.match_percentage < 80) matchBadgeClass += " medium";

      const idVal = activity.id || 1;

      return `
        <div class="activity-card" data-id="${idVal}">
            <div class="activity-header">
                <div class="activity-content">
                    <h3 class="activity-title">${activity.nama}</h3>
                    <p class="activity-description">${activity.deskripsi}</p>
                </div>
                <div class="activity-badges">
                    <span class="badge badge-category">${activity.kategori}</span>
                    <span class="badge ${matchBadgeClass}">${activity.match_percentage}% match</span>
                </div>
            </div>
            <div class="activity-info">
                <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#CE181B" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    <span>Deadline: ${activity.deadline}</span>
                </div>
                <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#CE181B" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    <span>Peserta ${activity.peserta}</span>
                </div>
                <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#CE181B" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                    </svg>
                    <span>${activity.lokasi}</span>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progressPercent}%"></div>
            </div>
        </div>
    `;
    })
    .join("");

  // Attach click listeners to navigate to detail page by id
  setTimeout(() => {
    document.querySelectorAll(".activity-card").forEach((card) => {
      card.addEventListener("click", () => {
        const id = card.getAttribute("data-id");
        if (!id) return;
        window.location.href = `/kegiatan/${id}`;
      });
    });
  }, 0);
}

// =============== FILTER ACTIVITIES ===============
function filterActivities() {
  filteredActivities = allActivities.filter((activity) => {
    const matchesCategory =
      currentFilter === "semua" ||
      activity.kategori.toLowerCase() === currentFilter;
    const matchesSearch =
      activity.nama.toLowerCase().includes(searchQuery.toLowerCase()) ||
      activity.deskripsi.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });
  renderActivities();
}

// =============== SHOW ERROR ===============
function showError(message) {
  document.getElementById("categoryGrid").innerHTML = `
    <div style="text-align: center; padding: 40px; color: var(--text-gray);">
        <p>${message}</p>
    </div>
  `;
  document.getElementById("activitiesList").innerHTML = `
    <div style="text-align: center; padding: 40px; color: var(--text-gray);">
        <p>${message}</p>
    </div>
  `;
}

// =============== FILTER AND SEARCH ===============
function setupFilterAndSearch() {
  // Filter pills event listeners
  document.querySelectorAll(".filter-pill").forEach((pill) => {
    pill.addEventListener("click", function () {
      document
        .querySelectorAll(".filter-pill")
        .forEach((p) => p.classList.remove("active"));
      this.classList.add("active");
      currentFilter = this.getAttribute("data-filter");
      filterActivities();
    });
  });

  // Search bar event listener
  const searchBar = document.getElementById("searchBar");
  if (searchBar) {
    searchBar.addEventListener("input", function (e) {
      searchQuery = e.target.value;
      filterActivities();
    });
  }
}

// =============== SETUP EVENT LISTENERS ===============
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
        .then(() => {
          window.location.href = "/login";
        })
        .catch(() => {
          window.location.href = "/login";
        });
    });
  }
}
