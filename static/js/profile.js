// Sidebar Toggle Functionality
document.addEventListener("DOMContentLoaded", function () {
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

  // Setup event listeners
  setupEventListeners();

  // Setup profile form
  setupProfileForm();
});

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
    logoutConfirm.addEventListener("click", performLogout);
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

function setupProfileForm() {
  const profileForm = document.getElementById("profileForm");

  if (profileForm) {
    profileForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const formData = {
        nama: document.getElementById("nama")?.value || "",
        username: document.getElementById("username")?.value || "",
        email: document.getElementById("email")?.value || "",
        password: document.getElementById("password")?.value || "",
        nim: document.getElementById("nim")?.value || "",
        fakultas: document.getElementById("fakultas")?.value || "",
      };

      try {
        const response = await fetch("/api/update-profile", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (data.success) {
          alert("Profil berhasil diperbarui!");
          // Optionally reload to reflect changes
          window.location.reload();
        } else {
          alert("Gagal memperbarui profil: " + data.message);
        }
      } catch (error) {
        console.error("Error updating profile:", error);
        alert("Terjadi kesalahan saat memperbarui profil.");
      }
    });
  }
}

async function performLogout() {
  try {
    const response = await fetch("/api/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    if (data.success) {
      window.location.href = "/login";
    } else {
      alert("Logout gagal. Silakan coba lagi.");
    }
  } catch (error) {
    console.error("Error during logout:", error);
    alert("Terjadi kesalahan saat logout.");
  }
}

const openBtn = document.getElementById("openAvatarModal");
const closeBtn = document.getElementById("closeAvatarModal");
const modal = document.getElementById("avatarModal");

openBtn.addEventListener("click", () => {
  modal.classList.add("active");
});

closeBtn.addEventListener("click", () => {
  modal.classList.remove("active");
});

modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.remove("active");
  }
});

// Profile Picture Upload Functionality
let selectedProfilePicture = null;

const btnSelectPhoto = document.getElementById("btnSelectPhoto");
const profilePictureInput = document.getElementById("profilePictureInput");
const avatarPreview = document.getElementById("avatarPreview");
const btnSavePhoto = document.getElementById("btnSavePhoto");
const btnCancelPhoto = document.getElementById("btnCancelPhoto");

if (btnSelectPhoto && profilePictureInput) {
  // Trigger file input when gallery button is clicked
  btnSelectPhoto.addEventListener("click", () => {
    profilePictureInput.click();
  });

  // Handle file selection
  profilePictureInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      if (!["image/jpeg", "image/png"].includes(file.type)) {
        alert("Format file harus JPG atau PNG!");
        return;
      }

      // Validate file size (max 2MB)
      if (file.size > 2 * 1024 * 1024) {
        alert("Ukuran file maksimal 2MB!");
        return;
      }

      // Read file and show preview
      const reader = new FileReader();
      reader.onload = (event) => {
        selectedProfilePicture = event.target.result;
        avatarPreview.innerHTML = `<img src="${selectedProfilePicture}" alt="Preview" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;" />`;
      };
      reader.readAsDataURL(file);
    }
  });
}

// Save profile picture
if (btnSavePhoto) {
  btnSavePhoto.addEventListener("click", async () => {
    if (!selectedProfilePicture) {
      alert("Silakan pilih foto terlebih dahulu!");
      return;
    }

    try {
      btnSavePhoto.disabled = true;
      btnSavePhoto.textContent = "Menyimpan...";

      const response = await fetch("/api/update-profile-picture", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile_picture: selectedProfilePicture,
        }),
      });

      const data = await response.json();
    } catch (error) {
      console.error("Error updating profile picture:", error);
      alert("Terjadi kesalahan saat memperbarui foto profil.");
    } finally {
      btnSavePhoto.disabled = false;
      btnSavePhoto.textContent = "Simpan Foto";
    }
  });
}

// Cancel photo selection
if (btnCancelPhoto) {
  btnCancelPhoto.addEventListener("click", () => {
    selectedProfilePicture = null;
    profilePictureInput.value = "";
    modal.classList.remove("active");
  });
}
// =============== NOTIFICATION FUNCTIONALITY ===============
document.addEventListener('DOMContentLoaded', function() {
  const notificationBell = document.getElementById('notificationBell');
  const notificationDropdown = document.getElementById('notificationDropdown');
  const notificationBadge = document.getElementById('notificationBadge');
  const notificationList = document.getElementById('notificationList');
  const markAllReadBtn = document.getElementById('markAllRead');
  
  if (!notificationBell) return;
  
  notificationBell.addEventListener('click', function(e) {
    e.stopPropagation();
    notificationDropdown.classList.toggle('show');
    if (notificationDropdown.classList.contains('show')) {
      loadNotifications();
    }
  });
  
  document.addEventListener('click', function(e) {
    if (!notificationDropdown.contains(e.target) && e.target !== notificationBell) {
      notificationDropdown.classList.remove('show');
    }
  });
  
  function loadNotifications() {
    fetch('/api/notifications')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          displayNotifications(data.notifications, data.unread_count);
        }
      })
      .catch(error => console.error('Error:', error));
  }
  
  function displayNotifications(notifications, unreadCount) {
    if (unreadCount > 0) {
      notificationBadge.textContent = unreadCount > 99 ? '99+' : unreadCount;
      notificationBadge.classList.add('show');
    } else {
      notificationBadge.classList.remove('show');
    }
    
    if (notifications.length === 0) {
      notificationList.innerHTML = '<div class="notification-empty"><i class="bi bi-bell-slash"></i><p>Tidak ada notifikasi</p></div>';
      return;
    }
    
    notificationList.innerHTML = notifications.map(n => `
      <div class="notification-item ${!n.is_read ? 'unread' : ''}" data-id="${n.id}" ${n.link ? `data-link="${n.link}"` : ''}>
        <div class="notification-icon-wrapper ${n.type}">
          <i class="bi bi-${n.type === 'success' ? 'check-circle-fill' : n.type === 'warning' ? 'exclamation-triangle-fill' : 'info-circle-fill'}"></i>
        </div>
        <div class="notification-content">
          <div class="notification-title">${n.title}</div>
          <div class="notification-message">${n.message}</div>
          <div class="notification-time">${n.time_ago}</div>
        </div>
      </div>
    `).join('');
    
    document.querySelectorAll('.notification-item').forEach(item => {
      item.addEventListener('click', function() {
        const notifId = this.dataset.id;
        const link = this.dataset.link;
        
        fetch('/api/notifications/mark-read', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({notification_id: notifId})
        }).then(() => {
          if (link) window.location.href = link;
        });
      });
    });
  }
  
  if (markAllReadBtn) {
    markAllReadBtn.addEventListener('click', function() {
      fetch('/api/notifications/mark-all-read', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
      }).then(() => loadNotifications());
    });
  }
  
  loadNotifications();
  setInterval(loadNotifications, 30000);
});