/* ===================================
   HASIL TES OMNI - JavaScript
=================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* =======================
       SIDEBAR TOGGLE
    ======================== */
  initSidebarToggle();

  /* =======================
       EVENT LISTENERS
    ======================== */
  setupEventListeners();

  /* =======================
       INITIALIZE CHARTS
    ======================== */
  initializeHasilTesCharts();
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

/* ===================================
   CHART INITIALIZATION
=================================== */
function initializeHasilTesCharts() {
  // Wait for Chart.js and plugins to load
  setTimeout(() => {
    if (typeof Chart === "undefined") {
      console.warn("Chart.js is not loaded");
      return;
    }

    // Register Chart.js datalabels plugin globally
    if (typeof ChartDataLabels !== "undefined") {
      Chart.register(ChartDataLabels);
    }

    initializeCharts();
  }, 100);
}

function initializeCharts() {
  // Pass user data to JavaScript (this will be populated by the template)
  const userData = window.userData || {
    aestheticism_t: 0,
    ambition_t: 0,
    anxiety_t: 0,
    assertiveness_t: 0,
    conventionality_t: 0,
    extraversion_t: 0,
    agreeableness_t: 0,
    conscientiousness_t: 0,
    neuroticism_t: 0,
    openness_t: 0,
  };

  /* =======================
       BAR CHART - Domain Scores
    ======================== */
  const barCtx = document.getElementById("omniUniqueBarChart");
  if (barCtx) {
    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: [
          "Extraversion",
          "Agreeableness",
          "Conscientiousness",
          "Neuroticism",
          "Openness",
        ],
        datasets: [
          {
            label: "Skor T",
            data: [
              userData.extraversion_t,
              userData.agreeableness_t,
              userData.conscientiousness_t,
              userData.neuroticism_t,
              userData.openness_t,
            ],
            backgroundColor: [
              "rgba(255, 99, 132, 0.7)",
              "rgba(54, 162, 235, 0.7)",
              "rgba(255, 206, 86, 0.7)",
              "rgba(75, 192, 192, 0.7)",
              "rgba(153, 102, 255, 0.7)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
            ],
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
          },
        },
        plugins: {
          legend: {
            display: false,
          },
          datalabels: {
            display: true,
            anchor: "end",
            align: "top",
            formatter: (value) => Math.round(value),
            font: {
              weight: "bold",
              size: 12,
            },
            color: "#333",
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return "Skor: " + Math.round(context.parsed.y);
              },
            },
          },
        },
      },
    });
    console.log("Bar chart initialized");
  }

  /* =======================
       PIE CHART - Top 5 Dimensions
    ======================== */
  const pieCtx = document.getElementById("omniUniquePieChart");
  if (pieCtx) {
    const allDimensions = [
      { name: "Aestheticism", value: userData.aestheticism_t },
      { name: "Ambition", value: userData.ambition_t },
      { name: "Anxiety", value: userData.anxiety_t },
      { name: "Assertiveness", value: userData.assertiveness_t },
      { name: "Conventionality", value: userData.conventionality_t },
    ];

    // Sort and get top 5
    const top5 = allDimensions
      .filter((d) => d.value > 0)
      .sort((a, b) => b.value - a.value)
      .slice(0, 5);

    new Chart(pieCtx, {
      type: "doughnut",
      data: {
        labels: top5.map((d) => d.name),
        datasets: [
          {
            data: top5.map((d) => d.value),
            backgroundColor: [
              "rgba(255, 99, 132, 0.7)",
              "rgba(54, 162, 235, 0.7)",
              "rgba(255, 206, 86, 0.7)",
              "rgba(75, 192, 192, 0.7)",
              "rgba(153, 102, 255, 0.7)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
            ],
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
          datalabels: {
            display: true,
            color: "#fff",
            font: {
              weight: "bold",
              size: 14,
            },
            formatter: (value, context) => {
              const total = context.chart.data.datasets[0].data.reduce(
                (a, b) => a + b,
                0
              );
              const percentage = ((value / total) * 100).toFixed(1);
              return Math.round(value) + "\n(" + percentage + "%)";
            },
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const value = context.parsed;
                const total = context.chart.data.datasets[0].data.reduce(
                  (a, b) => a + b,
                  0
                );
                const percentage = ((value / total) * 100).toFixed(1);
                return (
                  context.label +
                  ": " +
                  Math.round(value) +
                  " (" +
                  percentage +
                  "%)"
                );
              },
            },
          },
        },
      },
    });
    console.log("Pie chart initialized");
  }
}

/* ===================================
   EXPORT FUNCTIONALITY WITH LOADING MODAL (FETCH METHOD)
=================================== */
const btnExportOmniResult = document.getElementById("btnExportOmniResult");
const downloadModal = document.getElementById("downloadModal");

if (btnExportOmniResult) {
  btnExportOmniResult.addEventListener("click", async function () {
    // Show loading modal
    if (downloadModal) {
      downloadModal.classList.add("active");
    }

    // Disable button
    this.disabled = true;
    const originalHTML = this.innerHTML;
    this.innerHTML =
      '<span class="spinner-border spinner-border-sm me-2"></span>Memproses...';

    // Progress bar animation
    let progress = 0;
    const progressBar = document.getElementById("downloadProgressBar");
    
    const progressInterval = setInterval(() => {
      progress += 2;
      if (progressBar && progress <= 95) {
        progressBar.style.width = progress + "%";
      }
    }, 300);

    try {
      // ✅ FETCH PDF SEBAGAI BLOB
      const response = await fetch("/api/export-hasil-tes", {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error("Download gagal");
      }

      // Get blob from response
      const blob = await response.blob();
      
      // Complete progress
      clearInterval(progressInterval);
      if (progressBar) {
        progressBar.style.width = "100%";
      }

      // ✅ CREATE DOWNLOAD LINK DAN TRIGGER CLICK
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      
      // Get filename from Content-Disposition header atau gunakan default
      const contentDisposition = response.headers.get("Content-Disposition");
      let filename = "Hasil_Tes_OMNI.pdf";
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Hide modal after short delay
      setTimeout(() => {
        if (downloadModal) {
          downloadModal.classList.remove("active");
        }

        // Reset button
        this.disabled = false;
        this.innerHTML = originalHTML;

        // Show success notification
        showSuccessToast("PDF berhasil diunduh!");
        
        // Reset progress bar
        if (progressBar) {
          progressBar.style.width = "0%";
        }
      }, 1000);
      
    } catch (error) {
      console.error("Export error:", error);
      
      clearInterval(progressInterval);
      
      // Hide modal
      if (downloadModal) {
        downloadModal.classList.remove("active");
      }

      // Reset button
      this.disabled = false;
      this.innerHTML = originalHTML;

      // Reset progress bar
      if (progressBar) {
        progressBar.style.width = "0%";
      }

      // Show error notification
      alert("Gagal mengunduh PDF. Silakan coba lagi.");
    }
  });
}

/* ===================================
   SUCCESS TOAST
=================================== */
function showSuccessToast(message) {
  let toast = document.getElementById("successToast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "successToast";
    toast.className = "success-toast";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

/* ===================================
   SUCCESS TOAST (Optional)
=================================== */
function showSuccessToast(message) {
  let toast = document.getElementById("successToast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "successToast";
    toast.className = "success-toast";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

/* ===================================
   LOGOUT FUNCTION
=================================== */
function logout() {
  fetch("/api/logout", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.href = "/login";
      }
    })
    .catch((error) => {
      console.error("Logout error:", error);
      window.location.href = "/login";
    });
}
