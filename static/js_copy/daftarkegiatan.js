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
    
    // ✅ TAMBAHKAN INI
    // Setup edit functionality
    setupEditButtons();
    
    // Setup delete functionality  
    setupDeleteButtons();
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
// ===== EDIT FUNCTIONALITY =====
function setupEditButtons() {
    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', function() {
            const activityId = this.dataset.id;
            console.log('Edit clicked for activity:', activityId);
            loadActivityDataForEdit(activityId);
        });
    });
}

async function loadActivityDataForEdit(activityId) {
    try {
        console.log('Loading activity data for:', activityId);
        
        // Fetch activity detail
        const response = await fetch(`/api/activity-detail/${activityId}`);
        const data = await response.json();
        
        console.log('Received data:', data);
        
        if (!data.success) {
            alert('Gagal memuat data kegiatan');
            return;
        }
        
        const activity = data.activity;
        
        // Populate form fields
        document.getElementById('editKategori').value = activity.kategori || '';
        document.getElementById('editNamaKegiatan').value = activity.nama || '';
        document.getElementById('editDeskripsi').value = activity.deskripsi || '';
        document.getElementById('editDeadline').value = activity.deadline || '';
        document.getElementById('editPeserta').value = activity.peserta || '';
        document.getElementById('editLokasi').value = activity.lokasi || '';
        document.getElementById('editJadwal').value = activity.jadwal || '';
        document.getElementById('editLink').value = activity.link || '';
        
        // Populate contact info
        if (activity.contact) {
            document.getElementById('editKontakName').value = activity.contact.name || '';
            document.getElementById('editKontakPhone').value = activity.contact.phone || '';
            document.getElementById('editKontakEmail').value = activity.contact.email || '';
        }
        
        // Populate persyaratan (dynamic inputs)
        const persyaratanContainer = document.getElementById('editPersyaratanContainer');
        persyaratanContainer.innerHTML = '';
        
        if (activity.persyaratan && activity.persyaratan.length > 0) {
            activity.persyaratan.forEach((item, index) => {
                const row = document.createElement('div');
                row.className = 'input-row';
                row.innerHTML = `
                    <input type="text" name="editPersyaratan[]" value="${item}" placeholder="Masukkan persyaratan kegiatan..." />
                    ${index === 0 
                        ? '<button type="button" class="btn-add-input" id="editBtnAddPersyaratan"><i class="bi bi-plus-lg"></i></button>'
                        : '<button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>'
                    }
                `;
                persyaratanContainer.appendChild(row);
                
                if (index > 0) {
                    row.querySelector('.btn-remove-input').addEventListener('click', () => row.remove());
                }
            });
            
            // Re-attach add button handler
            document.getElementById('editBtnAddPersyaratan')?.addEventListener('click', function() {
                const newRow = document.createElement('div');
                newRow.className = 'input-row';
                newRow.innerHTML = `
                    <input type="text" name="editPersyaratan[]" placeholder="Masukkan persyaratan kegiatan..." />
                    <button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>
                `;
                persyaratanContainer.appendChild(newRow);
                newRow.querySelector('.btn-remove-input').addEventListener('click', () => newRow.remove());
            });
        } else {
            // Add default empty row
            persyaratanContainer.innerHTML = `
                <div class="input-row">
                    <input type="text" name="editPersyaratan[]" placeholder="Masukkan persyaratan kegiatan..." />
                    <button type="button" class="btn-add-input" id="editBtnAddPersyaratan"><i class="bi bi-plus-lg"></i></button>
                </div>
            `;
            
            document.getElementById('editBtnAddPersyaratan')?.addEventListener('click', function() {
                const newRow = document.createElement('div');
                newRow.className = 'input-row';
                newRow.innerHTML = `
                    <input type="text" name="editPersyaratan[]" placeholder="Masukkan persyaratan kegiatan..." />
                    <button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>
                `;
                persyaratanContainer.appendChild(newRow);
                newRow.querySelector('.btn-remove-input').addEventListener('click', () => newRow.remove());
            });
        }
        
        // Populate manfaat (dynamic inputs)
        const manfaatContainer = document.getElementById('editManfaatContainer');
        manfaatContainer.innerHTML = '';
        
        if (activity.manfaat && activity.manfaat.length > 0) {
            activity.manfaat.forEach((item, index) => {
                const row = document.createElement('div');
                row.className = 'input-row';
                row.innerHTML = `
                    <input type="text" name="editManfaat[]" value="${item}" placeholder="Masukkan manfaat & keuntungan kegiatan..." />
                    ${index === 0 
                        ? '<button type="button" class="btn-add-input" id="editBtnAddManfaat"><i class="bi bi-plus-lg"></i></button>'
                        : '<button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>'
                    }
                `;
                manfaatContainer.appendChild(row);
                
                if (index > 0) {
                    row.querySelector('.btn-remove-input').addEventListener('click', () => row.remove());
                }
            });
            
            // Re-attach add button handler
            document.getElementById('editBtnAddManfaat')?.addEventListener('click', function() {
                const newRow = document.createElement('div');
                newRow.className = 'input-row';
                newRow.innerHTML = `
                    <input type="text" name="editManfaat[]" placeholder="Masukkan manfaat & keuntungan kegiatan..." />
                    <button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>
                `;
                manfaatContainer.appendChild(newRow);
                newRow.querySelector('.btn-remove-input').addEventListener('click', () => newRow.remove());
            });
        } else {
            // Add default empty row
            manfaatContainer.innerHTML = `
                <div class="input-row">
                    <input type="text" name="editManfaat[]" placeholder="Masukkan manfaat & keuntungan kegiatan..." />
                    <button type="button" class="btn-add-input" id="editBtnAddManfaat"><i class="bi bi-plus-lg"></i></button>
                </div>
            `;
            
            document.getElementById('editBtnAddManfaat')?.addEventListener('click', function() {
                const newRow = document.createElement('div');
                newRow.className = 'input-row';
                newRow.innerHTML = `
                    <input type="text" name="editManfaat[]" placeholder="Masukkan manfaat & keuntungan kegiatan..." />
                    <button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>
                `;
                manfaatContainer.appendChild(newRow);
                newRow.querySelector('.btn-remove-input').addEventListener('click', () => newRow.remove());
            });
        }
        
        // Store activity ID for save
        document.getElementById('btnSimpanPerubahan').dataset.activityId = activityId;
        
        // Open edit modal
        openEditModal();
        
    } catch (error) {
        console.error('Error loading activity data:', error);
        alert('Terjadi kesalahan saat memuat data kegiatan');
    }
}

// ===== DELETE FUNCTIONALITY =====
function setupDeleteButtons() {
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const activityId = this.dataset.id;
            const activityName = this.dataset.nama;
            
            document.getElementById('deleteKegiatanName').textContent = activityName;
            document.getElementById('btnConfirmDelete').dataset.activityId = activityId;
            
            openDeleteModal();
        });
    });
}

// ===== MODAL FUNCTIONS =====
function openEditModal() {
    const modal = document.getElementById('modalEditKegiatan');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeEditModal() {
    const modal = document.getElementById('modalEditKegiatan');
    if (modal) {
        modal.classList.remove('active');
    }
}

function openDeleteModal() {
    const modal = document.getElementById('modalDeleteKegiatan');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeDeleteModal() {
    const modal = document.getElementById('modalDeleteKegiatan');
    if (modal) {
        modal.classList.remove('active');
    }
}

function showSuccessModal(message) {
    const modal = document.getElementById('modalSuccess');
    const messageEl = document.getElementById('successMessage');
    
    if (modal && messageEl) {
        messageEl.textContent = message;
        modal.classList.add('active');
    }
}

function closeSuccessModal() {
    const modal = document.getElementById('modalSuccess');
    if (modal) {
        modal.classList.remove('active');
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
// ===== SAVE EDIT =====
document.getElementById('btnSimpanPerubahan')?.addEventListener('click', async function() {
    const activityId = this.dataset.activityId;
    
    // Get persyaratan array
    const persyaratanInputs = document.querySelectorAll('#editPersyaratanContainer input[name="editPersyaratan[]"]');
    const persyaratan = Array.from(persyaratanInputs)
        .map(input => input.value.trim())
        .filter(val => val !== '');
    
    // Get manfaat array
    const manfaatInputs = document.querySelectorAll('#editManfaatContainer input[name="editManfaat[]"]');
    const manfaat = Array.from(manfaatInputs)
        .map(input => input.value.trim())
        .filter(val => val !== '');
    
    const formData = {
        id: activityId,
        kategori: document.getElementById('editKategori').value,
        nama: document.getElementById('editNamaKegiatan').value,
        deskripsi: document.getElementById('editDeskripsi').value,
        deadline: document.getElementById('editDeadline').value,
        peserta: document.getElementById('editPeserta').value,
        lokasi: document.getElementById('editLokasi').value,
        persyaratan: persyaratan,
        manfaat: manfaat,
        jadwal: document.getElementById('editJadwal').value,
        link: document.getElementById('editLink').value,
        kontak: {
            name: document.getElementById('editKontakName').value,
            phone: document.getElementById('editKontakPhone').value,
            email: document.getElementById('editKontakEmail').value
        }
    };
    
    try {
        const response = await fetch('/api/edit-activity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccessModal('Kegiatan berhasil diperbarui!');
            closeEditModal();
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            alert('Gagal memperbarui kegiatan: ' + data.message);
        }
    } catch (error) {
        console.error('Error updating activity:', error);
        alert('Terjadi kesalahan saat memperbarui kegiatan.');
    }
});

// ===== CONFIRM DELETE =====
document.getElementById('btnConfirmDelete')?.addEventListener('click', async function() {
    const activityId = this.dataset.activityId;
    
    try {
        const response = await fetch('/api/delete-activity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: activityId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccessModal('Kegiatan berhasil dihapus!');
            closeDeleteModal();
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            alert('Gagal menghapus kegiatan: ' + data.message);
        }
    } catch (error) {
        console.error('Error deleting activity:', error);
        alert('Terjadi kesalahan saat menghapus kegiatan.');
    }
});

// ===== CANCEL BUTTONS =====
document.getElementById('btnCancelEdit')?.addEventListener('click', closeEditModal);
document.getElementById('btnCancelDelete')?.addEventListener('click', closeDeleteModal);

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modalTambahKegiatan');
    if (e.target === modal) {
        closeModal();
    }
});
