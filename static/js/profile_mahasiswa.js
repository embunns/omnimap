/* =============================================
   PROFILE PAGE JAVASCRIPT
   ============================================= */

document.addEventListener("DOMContentLoaded", () => {
  /* =============================================
     PHOTO UPLOAD & PREVIEW
     ============================================= */

  const photoInput = document.getElementById("photoInput");
  const photoPreview = document.getElementById("photoPreview");
  const previewInitial = document.getElementById("previewInitial");
  const savePhotoBtn = document.getElementById("savePhotoBtn");
  const photoModal = new bootstrap.Modal(document.getElementById("photoModal"));
  const successModal = new bootstrap.Modal(
    document.getElementById("successModal")
  );

  let selectedImageBase64 = null;

  // Handle photo input change
  if (photoInput) {
    photoInput.addEventListener("change", function (e) {
      const file = e.target.files[0];

      if (file) {
        // Validate file size (max 2MB)
        if (file.size > 2 * 1024 * 1024) {
          alert("Ukuran file terlalu besar! Maksimal 2MB");
          photoInput.value = "";
          return;
        }

        // Validate file type
        if (!file.type.match("image.*")) {
          alert("File harus berupa gambar!");
          photoInput.value = "";
          return;
        }

        // Read and preview image
        const reader = new FileReader();
        reader.onload = function (e) {
          selectedImageBase64 = e.target.result;

          // Hide initial text
          if (previewInitial) {
            previewInitial.style.display = "none";
          }

          // Show image preview
          let img = photoPreview.querySelector("img");
          if (!img) {
            img = document.createElement("img");
            photoPreview.appendChild(img);
          }
          img.src = selectedImageBase64;
          img.style.display = "block";
        };
        reader.readAsDataURL(file);
      }
    });
  }

  /* =============================================
     SAVE PHOTO TO SERVER
     ============================================= */

  if (savePhotoBtn) {
    savePhotoBtn.addEventListener("click", function () {
      if (!selectedImageBase64) {
        alert("Silakan pilih foto terlebih dahulu!");
        return;
      }

      // Disable button and show loading
      savePhotoBtn.disabled = true;
      savePhotoBtn.innerHTML =
        '<i class="bi bi-hourglass-split me-2"></i>Menyimpan...';

      // Send to server
      fetch("/api/update-profile-picture", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile_picture: selectedImageBase64,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Update main avatar on profile page
            const mainAvatar = document.getElementById("mainAvatar");
            if (mainAvatar) {
              mainAvatar.innerHTML = `<img src="${selectedImageBase64}" alt="Profile Picture">`;
            }

            // Update navbar avatar if exists
            const navbarAvatar = document.querySelector(".user-info img");
            if (navbarAvatar) {
              navbarAvatar.src = selectedImageBase64;
            }

            // Close photo modal and show success modal
            photoModal.hide();
            successModal.show();

            // Reset button state
            savePhotoBtn.disabled = false;
            savePhotoBtn.innerHTML =
              '<i class="bi bi-check-circle me-2"></i>Simpan Foto';
          } else {
            alert(data.message || "Terjadi kesalahan saat menyimpan foto");
            savePhotoBtn.disabled = false;
            savePhotoBtn.innerHTML =
              '<i class="bi bi-check-circle me-2"></i>Simpan Foto';
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Terjadi kesalahan saat menyimpan foto");
          savePhotoBtn.disabled = false;
          savePhotoBtn.innerHTML =
            '<i class="bi bi-check-circle me-2"></i>Simpan Foto';
        });
    });
  }

  /* =============================================
     RESET MODAL ON CLOSE
     ============================================= */

  const photoModalElement = document.getElementById("photoModal");
  if (photoModalElement) {
    photoModalElement.addEventListener("hidden.bs.modal", function () {
      photoInput.value = "";
      selectedImageBase64 = null;

      // Reset preview to initial state
      if (previewInitial) {
        previewInitial.style.display = "flex";
      }

      const previewImg = photoPreview.querySelector("img");
      if (previewImg) {
        previewImg.remove();
      }
    });
  }
});

// =============== INITIALIZATION ===============
document.addEventListener("DOMContentLoaded", function () {
  // Initialize sidebar toggle
  initSidebarToggle();

  // Setup event listeners
  setupEventListeners();
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
// =============== NOTIFICATION FUNCTIONALITY ===============
document.addEventListener('DOMContentLoaded', function() {
  const notificationBell = document.getElementById('notificationBell');
  const notificationDropdown = document.getElementById('notificationDropdown');
  const notificationBadge = document.getElementById('notificationBadge');
  const notificationList = document.getElementById('notificationList');
  const markAllReadBtn = document.getElementById('markAllRead');
  
  if (!notificationBell) return;
  
  // Toggle dropdown
  notificationBell.addEventListener('click', function(e) {
    e.stopPropagation();
    notificationDropdown.classList.toggle('show');
    if (notificationDropdown.classList.contains('show')) {
      loadNotifications();
    }
  });
  
  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!notificationDropdown.contains(e.target) && e.target !== notificationBell) {
      notificationDropdown.classList.remove('show');
    }
  });
  
  // Load notifications
  function loadNotifications() {
    notificationList.innerHTML = `
      <div class="notification-loading">
        <div class="spinner"></div>
        <p>Memuat notifikasi...</p>
      </div>
    `;
    
    fetch('/api/notifications')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          displayNotifications(data.notifications, data.unread_count);
        } else {
          showError();
        }
      })
      .catch(error => {
        console.error('Error loading notifications:', error);
        showError();
      });
  }
  
  // Display notifications
  function displayNotifications(notifications, unreadCount) {
    // Update badge
    if (unreadCount > 0) {
      notificationBadge.textContent = unreadCount > 99 ? '99+' : unreadCount;
      notificationBadge.classList.add('show');
    } else {
      notificationBadge.classList.remove('show');
    }
    
    // Display notifications
    if (notifications.length === 0) {
      notificationList.innerHTML = `
        <div class="notification-empty">
          <i class="bi bi-bell-slash"></i>
          <p>Tidak ada notifikasi</p>
        </div>
      `;
      return;
    }
    
    notificationList.innerHTML = notifications.map(notif => `
      <div class="notification-item ${!notif.is_read ? 'unread' : ''}" 
           data-id="${notif.id}" 
           ${notif.link ? `data-link="${notif.link}"` : ''}>
        <div class="notification-icon-wrapper ${notif.type}">
          ${getNotificationIcon(notif.type)}
        </div>
        <div class="notification-content">
          <div class="notification-title">${notif.title}</div>
          <div class="notification-message">${notif.message}</div>
          <div class="notification-time">${notif.time_ago}</div>
        </div>
      </div>
    `).join('');
    
    // Add click handlers
    document.querySelectorAll('.notification-item').forEach(item => {
      item.addEventListener('click', function() {
        const notifId = this.dataset.id;
        const link = this.dataset.link;
        
        markAsRead(notifId).then(() => {
          if (link) {
            window.location.href = link;
          }
        });
      });
    });
  }
  
  // Get icon based on type
  function getNotificationIcon(type) {
    const icons = {
      'info': '<i class="bi bi-info-circle-fill"></i>',
      'success': '<i class="bi bi-check-circle-fill"></i>',
      'warning': '<i class="bi bi-exclamation-triangle-fill"></i>',
      'danger': '<i class="bi bi-x-circle-fill"></i>'
    };
    return icons[type] || icons['info'];
  }
  
  // Mark notification as read
  function markAsRead(notificationId) {
    return fetch('/api/notifications/mark-read', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ notification_id: notificationId })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        loadNotifications();
      }
    });
  }
  
  // Mark all as read
  if (markAllReadBtn) {
    markAllReadBtn.addEventListener('click', function() {
      fetch('/api/notifications/mark-all-read', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          loadNotifications();
        }
      });
    });
  }
  
  // Show error
  function showError() {
    notificationList.innerHTML = `
      <div class="notification-empty">
        <i class="bi bi-exclamation-circle"></i>
        <p>Gagal memuat notifikasi</p>
      </div>
    `;
  }
  
  // Load initial count
  loadNotifications();
  
  // Auto refresh every 30 seconds
  setInterval(loadNotifications, 30000);
});
