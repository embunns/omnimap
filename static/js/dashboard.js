/* ===============================================
   DASHBOARD.JS - OmniMap Dashboard Scripts
   Updated with new navbar and sidebar integration
================================================ */

/* =============== INITIALIZATION =============== */
document.addEventListener("DOMContentLoaded", function () {
  // Initialize sidebar toggle
  initSidebarToggle();

  // Setup event listeners
  setupEventListeners();

  /* =======================
       DASHBOARD DATA LOADER
    ======================== */
  loadDashboardData();

  /* =======================
       DASHBOARD CHARTS
    ======================== */
  initializeDashboardCharts();
});

/* =============== SIDEBAR TOGGLE =============== */
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
        if (content) {
          content.classList.toggle("full-width");
        }
      }
    });
  });
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
}

/* =======================
   LOAD DASHBOARD DATA
======================== */
async function loadDashboardData() {
  try {
    const res = await fetch("/api/recommended-activities");
    const data = await res.json();
    const activities = data.activities || [];

    // Update rekomendasi count
    const rekomendasiCount = document.getElementById("rekomendasiCount");
    if (rekomendasiCount) {
      rekomendasiCount.textContent = data.total || activities.length || 0;
    }

    // Populate activity recommendations (sorted by match_percentage)
    const activityContainer = document.getElementById(
      "activityRecommendations"
    );
    if (activityContainer && activities.length > 0) {
      activityContainer.innerHTML = activities
        .slice(0, 2)
        .map(
          (a) => `
                    <div class="activity-recommendation-card">
                        <div class="activity-card-header">
                            <div class="activity-title-section">
                                <h5 class="activity-title-text">${a.nama}</h5>
                                <p class="activity-description-text">${
                                  a.deskripsi || a.kategori
                                }</p>
                            </div>
                            <div class="activity-badges-section">
                                <span class="activity-tag activity-tag-red">${
                                  a.kategori
                                }</span>
                                <span class="activity-tag activity-tag-green">${
                                  a.match_percentage
                                }% match</span>
                            </div>
                        </div>
                        <div class="activity-meta-info">
                            <div class="activity-meta-item">
                                <i class="bi bi-calendar3"></i>
                                <span>Deadline : ${a.deadline || "-"}</span>
                            </div>
                            <div class="activity-meta-item">
                                <i class="bi bi-people"></i>
                                <span>Peserta ${a.peserta || "0/0"}</span>
                            </div>
                            <div class="activity-meta-item">
                                <i class="bi bi-geo-alt"></i>
                                <span>${a.lokasi || "Telkom University"}</span>
                            </div>
                        </div>
                        <div class="activity-progress-bar">
                            <div class="progress activity-progress-track">
                                <div class="progress-bar activity-progress-fill" style="width: ${
                                  a.match_percentage
                                }%"></div>
                            </div>
                        </div>
                    </div>
                `
        )
        .join("");
    } else if (activityContainer) {
      activityContainer.innerHTML =
        '<p class="text-muted text-center">Belum ada rekomendasi kegiatan</p>';
    }
  } catch (error) {
    console.error("Error loading activities:", error);
    const rekomendasiCount = document.getElementById("rekomendasiCount");
    if (rekomendasiCount) {
      rekomendasiCount.textContent = "0";
    }
  }
}

/* =======================
   INITIALIZE DASHBOARD CHARTS
======================== */
function initializeDashboardCharts() {
  // Wait a bit to ensure Chart.js is fully loaded
  setTimeout(() => {
    // Check if Chart.js is loaded
    if (typeof Chart === "undefined") {
      console.warn("Chart.js is not loaded");
      return;
    }

    initializeCharts();
  }, 100);
}

/* =======================
   INITIALIZE CHARTS
======================== */
function initializeCharts() {
  // Kategori Kegiatan Donut Chart
  const kategoriCtx = document.getElementById("kategoriKegiatanChart");
  if (kategoriCtx) {
    const kategoriChart = new Chart(kategoriCtx, {
      type: "doughnut",
      data: {
        labels: ["Kepanitiaan", "UKM", "Organisasi"],
        datasets: [
          {
            data: [64, 43, 5],
            backgroundColor: ["#e91e63", "#64b5f6", "#ff9800"],
            borderWidth: 0,
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.label + ": " + context.parsed + "%";
              },
            },
          },
        },
      },
    });
    console.log("Kategori Kegiatan chart initialized");
  }

  // Skor Rata-rata Gauge Chart (semi-circle)
  const gaugeCtx = document.getElementById("skorRataRataGauge");
  if (gaugeCtx) {
    const gaugeChart = new Chart(gaugeCtx, {
      type: "doughnut",
      data: {
        labels: ["Skor", "Sisa"],
        datasets: [
          {
            data: [72, 28],
            backgroundColor: ["#2196f3", "#e0e0e0"],
            borderWidth: 0,
            cutout: "75%",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        circumference: 180,
        rotation: -90,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            enabled: false,
          },
        },
      },
    });
    console.log("Skor Rata-rata gauge chart initialized");
  }
}
