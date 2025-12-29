// Sidebar Toggle Functionality
document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");
  const toggleButtons = document.querySelectorAll(".toggle-sidebar");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const isMobile = window.innerWidth <= 768;

      if (isMobile) {
        sidebar.classList.toggle("mobile-active");
      } else {
        sidebar.classList.toggle("hide");
        content.classList.toggle("full-width");
      }
    });
  });

  // Load mahasiswa data
  loadMahasiswaData();

  // Setup event listeners
  setupEventListeners();
});

function setupEventListeners() {
  // Search input
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", debounce(filterMahasiswa, 500));
  }

  // Filter risk level
  const filterRisk = document.getElementById("filterRisk");
  if (filterRisk) {
    filterRisk.addEventListener("change", loadMahasiswaData);
  }

  // Filter angkatan
  const filterAngkatan = document.getElementById("filterAngkatan");
  if (filterAngkatan) {
    filterAngkatan.addEventListener("change", loadMahasiswaData);
  }

  // Export button
  const btnExport = document.getElementById("btnExport");
  if (btnExport) {
    btnExport.addEventListener("click", exportMahasiswaData);
  }

  // Modal close
  const closeModal = document.getElementById("closeModal");
  if (closeModal) {
    closeModal.addEventListener("click", () => {
      document.getElementById("detailModal").classList.remove("active");
    });
  }

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
}
// ✅ TAMBAHKAN FUNGSI INI - Populate dropdown angkatan
async function loadAngkatanOptions() {
  try {
    const response = await fetch('/api/get-angkatan-list');
    const data = await response.json();
    
    if (data.success && data.angkatan_list) {
      const filterAngkatan = document.getElementById("filterAngkatan");
      
      // Clear existing options (except "Semua Angkatan")
      filterAngkatan.innerHTML = '<option value="">Semua Angkatan</option>';
      
      // Add angkatan options
      data.angkatan_list.forEach(angkatan => {
        const option = document.createElement('option');
        option.value = angkatan;
        option.textContent = `Angkatan 20${angkatan}`;
        filterAngkatan.appendChild(option);
      });
      
      console.log(`✅ Loaded ${data.angkatan_list.length} angkatan options`);
    }
  } catch (error) {
    console.error('Error loading angkatan options:', error);
  }
}

async function loadAngkatanOptions() {
  try {
    const response = await fetch('/api/get-angkatan-list');
    const data = await response.json();
    
    if (data.success && data.angkatan_list) {
      const filterAngkatan = document.getElementById("filterAngkatan");
      
      // Clear existing options (except "Semua Angkatan")
      filterAngkatan.innerHTML = '<option value="">Semua Angkatan</option>';
      
      // Add angkatan options
      data.angkatan_list.forEach(angkatan => {
        const option = document.createElement('option');
        option.value = angkatan;
        option.textContent = `Angkatan 20${angkatan}`;
        filterAngkatan.appendChild(option);
      });
      
      console.log(`✅ Loaded ${data.angkatan_list.length} angkatan options`);
    }
  } catch (error) {
    console.error('Error loading angkatan options:', error);
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
  const loadingIndicator = document.getElementById("loadingIndicator");
  const tableBody = document.getElementById("mahasiswaTableBody");
  const emptyState = document.getElementById("emptyState");
  const filterRisk = document.getElementById("filterRisk");
  const filterAngkatan = document.getElementById("filterAngkatan");

  try {
    if (loadingIndicator) loadingIndicator.style.display = "block";

    // Build query parameters
    const params = new URLSearchParams();
    if (filterRisk && filterRisk.value) {
      params.append("risk_level", filterRisk.value);
    }
    if (filterAngkatan && filterAngkatan.value) {
      params.append("angkatan", filterAngkatan.value);
    }

    const response = await fetch(`/api/mahasiswa-rentan?${params.toString()}`);

    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }

    const data = await response.json();

    if (loadingIndicator) loadingIndicator.style.display = "none";

    if (data.success) {
      // Update statistics
      updateStatistics(data.stats);

      // Display mahasiswa data
      displayMahasiswaData(data.mahasiswa);

      // Store data globally for filtering
      window.mahasiswaData = data.mahasiswa;
    } else {
      throw new Error(data.error || "Failed to load data");
    }
  } catch (error) {
    console.error("Error loading mahasiswa data:", error);
    if (loadingIndicator) loadingIndicator.style.display = "none";
    if (tableBody) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="8" style="text-align: center; padding: 40px; color: #e74c3c;">
            Gagal memuat data. Silakan refresh halaman.
          </td>
        </tr>
      `;
    }
  }
}

function updateStatistics(stats) {
  const totalMahasiswa = document.getElementById("totalMahasiswa");
  const totalRentan = document.getElementById("totalRentan");
  const criticalCount = document.getElementById("criticalCount");

  if (totalMahasiswa) {
    totalMahasiswa.textContent = formatNumber(stats.total_mahasiswa);
  }
  if (totalRentan) {
    totalRentan.textContent = formatNumber(stats.total_rentan || 0);
  }
  if (criticalCount) {
    criticalCount.textContent = formatNumber(stats.critical_count || 0);
  }
}

function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function displayMahasiswaData(mahasiswaList) {
  const tableBody = document.getElementById("mahasiswaTableBody");
  const emptyState = document.getElementById("emptyState");

  if (!tableBody) return;

  if (!mahasiswaList || mahasiswaList.length === 0) {
    tableBody.innerHTML = "";
    if (emptyState) emptyState.style.display = "block";
    return;
  }

  if (emptyState) emptyState.style.display = "none";

  tableBody.innerHTML = mahasiswaList
    .map(
      (m) => `
        <tr>
          <td>${m.no}</td>
          <td>${m.nim}</td>
          <td>${m.nama}</td>
          <td>${m.fakultas}</td>
          <td><strong>${m.risk_score}</strong></td>
          <td><span class="badge ${m.kategori_class}">${m.kategori}</span></td>
          <td class="concern-cell">${m.primary_concern || '-'}</td>
          <td>
            <button class="btn-detail" onclick="showDetail('${m.nim}')">
              <i class="bi bi-eye"></i> Detail
            </button>
          </td>
        </tr>
      `
    )
    .join("");
}

function filterMahasiswa() {
  if (!window.mahasiswaData) {
    loadMahasiswaData();
    return;
  }

  const searchInput = document.getElementById("searchInput");
  const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";

  let filteredData = window.mahasiswaData;

  // Apply search filter
  if (searchTerm) {
    filteredData = filteredData.filter(
      (m) =>
        m.nama.toLowerCase().includes(searchTerm) ||
        m.nim.toLowerCase().includes(searchTerm)
    );
  }

  // Re-number the filtered data
  filteredData = filteredData.map((m, index) => ({
    ...m,
    no: index + 1,
  }));

  displayMahasiswaData(filteredData);
}

async function showDetail(nim) {
  const detailModal = document.getElementById("detailModal");
  const detailContent = document.getElementById("detailContent");

  if (!detailModal || !detailContent) return;

  // Find student data
  const student = window.mahasiswaData.find((m) => m.nim === nim);
  if (!student) return;

  // Show loading
  detailContent.innerHTML = '<div style="text-align: center; padding: 40px;">Memuat detail...</div>';
  detailModal.classList.add("active");

  // Display detailed assessment
  let categoriesHTML = "";
  if (student.categories && student.categories.length > 0) {
    categoriesHTML = student.categories
      .map(
        (cat) => `
      <div class="category-detail">
        <div class="category-header ${cat.severity}">
          <h4>${cat.name}</h4>
          <span class="severity-badge ${cat.severity}">${getSeverityText(cat.severity)}</span>
        </div>
        <ul class="flags-list">
          ${cat.flags.map((flag) => `<li>${flag}</li>`).join("")}
        </ul>
      </div>
    `
      )
      .join("");
  }

  detailContent.innerHTML = `
    <div class="student-info">
      <h3>${student.nama}</h3>
      <p><strong>NIM:</strong> ${student.nim}</p>
      <p><strong>Fakultas:</strong> ${student.fakultas}</p>
      <p><strong>Risk Score:</strong> <span class="risk-score">${student.risk_score}</span></p>
      <p><strong>Kategori:</strong> <span class="badge ${student.kategori_class}">${student.kategori}</span></p>
    </div>

    <div class="assessment-details">
      <h3>Detail Assessment</h3>
      ${categoriesHTML || '<p>Tidak ada assessment detail tersedia.</p>'}
    </div>

    <div class="trait-scores">
      <h3>Skor Trait Kritis</h3>
      <div class="score-grid">
        <div class="score-item">
          <span>Depression:</span>
          <strong class="${student.depression_t >= 65 ? 'critical-score' : ''}">${student.depression_t}</strong>
        </div>
        <div class="score-item">
          <span>Anxiety:</span>
          <strong class="${student.anxiety_t >= 65 ? 'critical-score' : ''}">${student.anxiety_t}</strong>
        </div>
        <div class="score-item">
          <span>Hostility:</span>
          <strong class="${student.hostility_t >= 65 ? 'critical-score' : ''}">${student.hostility_t}</strong>
        </div>
      </div>
    </div>

    <div class="recommendation">
      <h3>Rekomendasi Tindakan</h3>
      ${getRecommendation(student)}
    </div>
  `;
}

function getSeverityText(severity) {
  const map = {
    critical: "KRITIS",
    high: "TINGGI",
    medium: "SEDANG",
    low: "RENDAH",
  };
  return map[severity] || severity.toUpperCase();
}

function getRecommendation(student) {
  if (student.risk_score >= 50) {
    return `
      <div class="recommendation-critical">
        <p><strong>⚠️ TINDAKAN SEGERA DIPERLUKAN:</strong></p>
        <ul>
          <li>Hubungi mahasiswa untuk konseling segera</li>
          <li>Rujuk ke layanan psikologi kampus</li>
          <li>Monitor secara intensif</li>
          <li>Koordinasi dengan keluarga jika diperlukan</li>
        </ul>
      </div>
    `;
  } else if (student.risk_score >= 35) {
    return `
      <div class="recommendation-high">
        <p><strong>⚡ TINDAKAN PRIORITAS:</strong></p>
        <ul>
          <li>Jadwalkan sesi konseling dalam 1 minggu</li>
          <li>Berikan informasi layanan dukungan</li>
          <li>Follow-up berkala</li>
        </ul>
      </div>
    `;
  } else {
    return `
      <div class="recommendation-medium">
        <p><strong>📋 TINDAKAN PREVENTIF:</strong></p>
        <ul>
          <li>Informasikan layanan konseling yang tersedia</li>
          <li>Monitor perkembangan akademik</li>
          <li>Dorong partisipasi dalam kegiatan kampus</li>
        </ul>
      </div>
    `;
  }
}

async function exportMahasiswaData() {
  try {
    const response = await fetch("/api/export-mahasiswa-rentan");

    if (!response.ok) {
      throw new Error("Export failed");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `mahasiswa_rentan_${new Date().getTime()}.csv`;
    document.body.appendChild(a);
    a.click();

    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error("Error exporting data:", error);
    alert("Gagal mengexport data. Silakan coba lagi.");
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