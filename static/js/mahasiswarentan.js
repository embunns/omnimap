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

    // Load mahasiswa data
    loadMahasiswaData();
    
    // Setup event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterMahasiswa, 500));
    }
    
    // Filter angkatan
    const filterAngkatan = document.getElementById('filterAngkatan');
    if (filterAngkatan) {
        filterAngkatan.addEventListener('change', filterMahasiswa);
    }
    
    // Export button
    const btnExport = document.getElementById('btnExport');
    if (btnExport) {
        btnExport.addEventListener('click', exportMahasiswaData);
    }
    
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

async function loadMahasiswaData() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const tableBody = document.getElementById('mahasiswaTableBody');
    const emptyState = document.getElementById('emptyState');
    
    try {
        if (loadingIndicator) loadingIndicator.style.display = 'block';
        
        const response = await fetch('/api/mahasiswa-rentan');
        
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();
        
        if (loadingIndicator) loadingIndicator.style.display = 'none';
        
        if (data.success) {
            // Update statistics
            updateStatistics(data.stats);
            
            // Display mahasiswa data
            displayMahasiswaData(data.mahasiswa);
            
            // Store data globally for filtering
            window.mahasiswaData = data.mahasiswa;
        } else {
            throw new Error(data.error || 'Failed to load data');
        }
        
    } catch (error) {
        console.error('Error loading mahasiswa data:', error);
        if (loadingIndicator) loadingIndicator.style.display = 'none';
        if (tableBody) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: #e74c3c;">
                        Gagal memuat data. Silakan refresh halaman.
                    </td>
                </tr>
            `;
        }
    }
}

function updateStatistics(stats) {
    const totalMahasiswa = document.getElementById('totalMahasiswa');
    const sudahOmni = document.getElementById('sudahOmni');
    const belumOmni = document.getElementById('belumOmni');
    
    if (totalMahasiswa) {
        totalMahasiswa.textContent = formatNumber(stats.total_mahasiswa);
    }
    if (sudahOmni) {
        sudahOmni.textContent = formatNumber(stats.sudah_omni);
    }
    if (belumOmni) {
        belumOmni.textContent = formatNumber(stats.belum_omni);
    }
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function displayMahasiswaData(mahasiswaList) {
    const tableBody = document.getElementById('mahasiswaTableBody');
    const emptyState = document.getElementById('emptyState');
    
    if (!tableBody) return;
    
    if (!mahasiswaList || mahasiswaList.length === 0) {
        tableBody.innerHTML = '';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }
    
    if (emptyState) emptyState.style.display = 'none';
    
    tableBody.innerHTML = mahasiswaList.map(m => `
        <tr>
            <td>${m.no}</td>
            <td>${m.nim}</td>
            <td>${m.nama}</td>
            <td>${m.fakultas}</td>
            <td>${m.program_studi}</td>
            <td>${m.skor_omni}</td>
            <td><span class="badge ${m.kategori_class}">${m.kategori}</span></td>
        </tr>
    `).join('');
}

function filterMahasiswa() {
    if (!window.mahasiswaData) {
        loadMahasiswaData();
        return;
    }
    
    const searchInput = document.getElementById('searchInput');
    const filterAngkatan = document.getElementById('filterAngkatan');
    
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const angkatanFilter = filterAngkatan ? filterAngkatan.value : '';
    
    let filteredData = window.mahasiswaData;
    
    // Apply search filter
    if (searchTerm) {
        filteredData = filteredData.filter(m => 
            m.nama.toLowerCase().includes(searchTerm) ||
            m.nim.toLowerCase().includes(searchTerm)
        );
    }
    
    // Apply angkatan filter
    if (angkatanFilter) {
        filteredData = filteredData.filter(m => 
            m.nim.startsWith(angkatanFilter)
        );
    }
    
    // Re-number the filtered data
    filteredData = filteredData.map((m, index) => ({
        ...m,
        no: index + 1
    }));
    
    displayMahasiswaData(filteredData);
}

async function exportMahasiswaData() {
    try {
        const response = await fetch('/api/export-mahasiswa-rentan');
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        // Create blob from response
        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mahasiswa_rentan_${new Date().getTime()}.csv`;
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Show success message
        alert('Data berhasil diexport!');
        
    } catch (error) {
        console.error('Error exporting data:', error);
        alert('Gagal mengexport data. Silakan coba lagi.');
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