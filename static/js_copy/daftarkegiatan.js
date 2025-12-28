// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const toggleButtons = document.querySelectorAll('.toggle-sidebar');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            sidebar.classList.toggle('hide');
            content.classList.toggle('full-width');
        });
    });

    // Setup event listeners
    setupEventListeners();
    
    // Setup filter functionality
    setupFilterButtons();
    
    // Setup add activity form
    setupAddActivityForm();
});

function setupEventListeners() {
    // Logout functionality
    const signOutBtn = document.getElementById('signOutBtn');
    const logoutModal = document.getElementById('logoutModal');
    const logoutCancel = document.getElementById('logoutCancel');
    const logoutConfirm = document.getElementById('logoutConfirm');
    
    if (signOutBtn && logoutModal) {
        signOutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logoutModal.classList.add('active');
        });
    }
    
    if (logoutCancel && logoutModal) {
        logoutCancel.addEventListener('click', function() {
            logoutModal.classList.remove('active');
        });
    }
    
    if (logoutConfirm) {
        logoutConfirm.addEventListener('click', performLogout);
    }

    // Close modal when clicking outside
    if (logoutModal) {
        logoutModal.addEventListener('click', function(e) {
            if (e.target === logoutModal) {
                logoutModal.classList.remove('active');
            }
        });
    }

    // Search functionality
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterKegiatan, 300));
    }
}

function setupAddActivityForm() {
    const btnUpload = document.getElementById('btnUploadKegiatan');
    
    if (btnUpload) {
        btnUpload.addEventListener('click', async function() {
            const formData = {
                kategori: document.getElementById('kategori')?.value || '',
                nama: document.getElementById('namaKegiatan')?.value || '',
                deskripsi: document.getElementById('deskripsi')?.value || '',
                deadline: document.getElementById('deadline')?.value || '',
                peserta: document.getElementById('peserta')?.value || '',
                lokasi: document.getElementById('lokasi')?.value || '',
                persyaratan: document.getElementById('persyaratan')?.value || '',
                manfaat: document.getElementById('manfaat')?.value || '',
                jadwal: document.getElementById('jadwal')?.value || '',
                link: document.getElementById('link')?.value || '',
                kontak: document.getElementById('kontak')?.value || ''
            };
            
            // Validate required fields
            if (!formData.kategori || !formData.nama) {
                alert('Kategori dan Nama Kegiatan harus diisi!');
                return;
            }
            
            try {
                const response = await fetch('/api/add-activity', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('Kegiatan berhasil ditambahkan!');
                    closeModal();
                    // Reload page to show new activity
                    window.location.reload();
                } else {
                    alert('Gagal menambahkan kegiatan: ' + data.message);
                }
            } catch (error) {
                console.error('Error adding activity:', error);
                alert('Terjadi kesalahan saat menambahkan kegiatan.');
            }
        });
    }
}

function setupFilterButtons() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const kegiatanCards = document.querySelectorAll('.kegiatan-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get filter category
            let filterCategory = '';
            if (this.classList.contains('ukm')) filterCategory = 'UKM';
            else if (this.classList.contains('organisasi')) filterCategory = 'Organisasi';
            else if (this.classList.contains('kepanitiaan')) filterCategory = 'Kepanitiaan';
            else if (this.classList.contains('lomba')) filterCategory = 'Lomba';
            // 'semua' will have empty filterCategory
            
            // Filter cards
            kegiatanCards.forEach(card => {
                if (filterCategory === '' || card.dataset.kategori === filterCategory) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

function filterKegiatan() {
    const searchInput = document.querySelector('.search-box input');
    const searchTerm = searchInput.value.toLowerCase();
    const kegiatanCards = document.querySelectorAll('.kegiatan-card');
    
    kegiatanCards.forEach(card => {
        const title = card.querySelector('.kegiatan-title').textContent.toLowerCase();
        const desc = card.querySelector('.kegiatan-desc').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || desc.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

async function performLogout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.location.href = '/login';
        } else {
            alert('Logout gagal. Silakan coba lagi.');
        }
        
    } catch (error) {
        console.error('Error during logout:', error);
        alert('Terjadi kesalahan saat logout.');
    }
}

// Modal functions for adding kegiatan
function openModal() {
    const modal = document.getElementById('modalTambahKegiatan');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal() {
    const modal = document.getElementById('modalTambahKegiatan');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modalTambahKegiatan');
    if (e.target === modal) {
        closeModal();
    }
});
