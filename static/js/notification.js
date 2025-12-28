document.addEventListener('DOMContentLoaded', function() {
  const notificationBell = document.getElementById('notificationBell');
  const notificationDropdown = document.getElementById('notificationDropdown');
  const notificationBadge = document.getElementById('notificationBadge');
  const notificationList = document.getElementById('notificationList');
  const markAllReadBtn = document.getElementById('markAllRead');
  
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