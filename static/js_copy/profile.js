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
    
    // Setup profile form
    setupProfileForm();
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
}

function setupProfileForm() {
    const profileForm = document.getElementById('profileForm');
    
    if (profileForm) {
        profileForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                nama: document.getElementById('nama')?.value || '',
                username: document.getElementById('username')?.value || '',
                email: document.getElementById('email')?.value || '',
                password: document.getElementById('password')?.value || '',
                nim: document.getElementById('nim')?.value || '',
                fakultas: document.getElementById('fakultas')?.value || ''
            };
            
            try {
                const response = await fetch('/api/update-profile', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('Profil berhasil diperbarui!');
                    // Optionally reload to reflect changes
                    window.location.reload();
                } else {
                    alert('Gagal memperbarui profil: ' + data.message);
                }
            } catch (error) {
                console.error('Error updating profile:', error);
                alert('Terjadi kesalahan saat memperbarui profil.');
            }
        });
    }
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
