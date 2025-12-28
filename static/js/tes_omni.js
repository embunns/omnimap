/* ===============================================
   TES OMNI - Navbar & Sidebar Scripts
   Aligns behavior with Dashboard
================================================ */

document.addEventListener("DOMContentLoaded", function () {
  initSidebarToggle();
  setupEventListeners();
  // Sync header overlap after initial render
  syncHeaderWithPaper();
  // Re-sync on resize
  window.addEventListener("resize", debounce(syncHeaderWithPaper, 100));
  // Observe content height changes to re-sync overlap
  const testWrapper = document.getElementById("test-wrapper");
  if (testWrapper && "MutationObserver" in window) {
    const observer = new MutationObserver(debounce(syncHeaderWithPaper, 100));
    observer.observe(testWrapper, { childList: true, subtree: true });
  }
});

function initSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const toggleButtons = document.querySelectorAll(".toggle-sidebar");

  toggleButtons.forEach((button) => {
    const handler = function (e) {
      if (e && e.preventDefault) e.preventDefault();
      if (e && e.stopImmediatePropagation) e.stopImmediatePropagation();
      else if (e && e.stopPropagation) e.stopPropagation();
      const isMobile = window.innerWidth <= 768;
      if (isMobile) {
        sidebar.classList.toggle("mobile-active");
        if (sidebarOverlay) sidebarOverlay.classList.toggle("active");
        // Lock scroll when sidebar opens
        document.body.classList.toggle(
          "sidebar-open",
          sidebar.classList.contains("mobile-active")
        );
      } else {
        sidebar.classList.toggle("hide");
        if (content) content.classList.toggle("full-width");
      }
    };
    // Click and touch events for mobile reliability
    button.addEventListener("click", handler, { passive: false });
    button.addEventListener("touchstart", handler, { passive: false });
  });

  // Close on overlay click
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", function () {
      sidebar.classList.remove("mobile-active");
      sidebarOverlay.classList.remove("active");
      document.body.classList.remove("sidebar-open");
    });
  }

  // Close when clicking outside on mobile
  document.addEventListener("click", function (e) {
    const isMobile = window.innerWidth <= 768;
    if (
      isMobile &&
      sidebar.classList.contains("mobile-active") &&
      !sidebar.contains(e.target) &&
      !e.target.classList.contains("toggle-sidebar")
    ) {
      sidebar.classList.remove("mobile-active");
      if (sidebarOverlay) sidebarOverlay.classList.remove("active");
      document.body.classList.remove("sidebar-open");
    }
  });

  // Prevent closing when clicking inside sidebar
  if (sidebar) {
    sidebar.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  }
}

function setupEventListeners() {
  // Logout using custom modal
  const signOutBtn = document.getElementById("signOutBtn");
  const customLogoutModal = document.getElementById("logoutModalCustom");
  const logoutCancel = document.getElementById("logoutCancel");
  const logoutConfirm = document.getElementById("logoutConfirm");

  if (signOutBtn && customLogoutModal) {
    signOutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      customLogoutModal.classList.add("active");
    });
  }

  if (logoutCancel && customLogoutModal) {
    logoutCancel.addEventListener("click", function () {
      customLogoutModal.classList.remove("active");
    });
  }

  if (logoutConfirm) {
    logoutConfirm.addEventListener("click", function () {
      fetch("/api/logout", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.href = "/login";
          } else {
            window.location.href = "/login";
          }
        })
        .catch(() => {
          window.location.href = "/login";
        });
    });
  }
}

/* =======================
   HEADER OVERLAP SYNC
======================= */
function syncHeaderWithPaper() {
  const header = document.querySelector(".header-tes-omni");
  const paper = document.querySelector(".omni-tes-paper-bg");
  if (!header || !paper) return;

  const w = window.innerWidth;
  const isMobile = w <= 768;
  const isTablet = w <= 991 && w > 768;

  // Calculate header height based on paper height to keep nice overlap
  const paperHeight = paper.offsetHeight || 300;
  const overlapRatio = isMobile ? 0.45 : isTablet ? 0.5 : 0.55;
  const minHeader = Math.max(160, Math.round(paperHeight * overlapRatio));

  header.style.minHeight = minHeader + "px";

  // Set negative top margin for the paper to overlap about half the header
  const overlapAmount = Math.round(minHeader * 0.5);
  paper.style.marginTop = "-" + overlapAmount + "px";
}

/* =======================
   Utils: debounce
======================= */
function debounce(fn, delay) {
  let t;
  return function () {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, arguments), delay);
  };
}