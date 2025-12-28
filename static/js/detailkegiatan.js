/* ===============================================
   DETAILKEGIATAN.JS - OmniMap Detail Kegiatan Scripts
   Updated with new navbar and sidebar integration
================================================ */

/* =============== INITIALIZATION =============== */
document.addEventListener("DOMContentLoaded", function () {
  // Initialize sidebar toggle
  initSidebarToggle();

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
    button.addEventListener("click", function () {
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

  // Close sidebar when clicking overlay
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", function () {
      sidebar.classList.remove("mobile-active");
      sidebarOverlay.classList.remove("active");
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
