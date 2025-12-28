let deleteContext = { id: "", name: "" };

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

  // Setup filter functionality
  setupFilterButtons();

  // Setup add activity form
  setupAddActivityForm();

  // Setup edit activity modal
  setupEditModal();

  // Setup delete activity modal
  setupDeleteModal();

  // Setup card navigation
  setupCardNavigation();
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

  // Search functionality
  const searchInput = document.querySelector(".search-box input");
  if (searchInput) {
    searchInput.addEventListener("input", debounce(filterKegiatan, 300));
  }
}

function setupEditModal() {
  const editModal = document.getElementById("modalEditKegiatan");
  if (!editModal) return;

  let currentEditCard = null; // Simpan referensi card yang sedang diedit

  const editButtons = document.querySelectorAll(".btn-edit");
  editButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.stopPropagation(); // Prevent card click
      
      currentEditCard = this.closest(".kegiatan-card");
      const modalData = {
        id: this.dataset.id || currentEditCard?.dataset.id || "",
        kategori: currentEditCard?.dataset.kategori || "",
        nama: this.dataset.nama || "",
        deskripsi: this.dataset.deskripsi || "",
        deadline: this.dataset.deadline || "",
        peserta: this.dataset.peserta || "",
        lokasi: this.dataset.lokasi || "",
        jadwal: this.dataset.jadwal || "",
        link: this.dataset.link || "",
        kontakName: this.dataset.kontakName || "",
        kontakPhone: this.dataset.kontakPhone || "",
        kontakEmail: this.dataset.kontakEmail || "",
      };

      fillEditModal(modalData);
      openEditModal();
    });
  });

  // Setup dynamic input buttons
  const editBtnAddPersyaratan = document.getElementById("editBtnAddPersyaratan");
  if (editBtnAddPersyaratan) {
    editBtnAddPersyaratan.addEventListener("click", function () {
      addInputRow(
        "editPersyaratanContainer",
        "editPersyaratan[]",
        "Masukkan persyaratan kegiatan..."
      );
    });
  }

  const editBtnAddManfaat = document.getElementById("editBtnAddManfaat");
  if (editBtnAddManfaat) {
    editBtnAddManfaat.addEventListener("click", function () {
      addInputRow(
        "editManfaatContainer",
        "editManfaat[]",
        "Masukkan manfaat & keuntungan kegiatan..."
      );
    });
  }

  const btnCancelEdit = document.getElementById("btnCancelEdit");
  if (btnCancelEdit) {
    btnCancelEdit.addEventListener("click", function (e) {
      e.preventDefault();
      closeEditModal();
    });
  }

  const btnSimpanPerubahan = document.getElementById("btnSimpanPerubahan");
  if (btnSimpanPerubahan) {
    btnSimpanPerubahan.addEventListener("click", async function (e) {
      e.preventDefault();

      // Collect edit form data
      const persyaratanInputs = document.querySelectorAll('input[name="editPersyaratan[]"]');
      const persyaratanValues = Array.from(persyaratanInputs)
        .map((input) => input.value.trim())
        .filter((value) => value !== "");

      const manfaatInputs = document.querySelectorAll('input[name="editManfaat[]"]');
      const manfaatValues = Array.from(manfaatInputs)
        .map((input) => input.value.trim())
        .filter((value) => value !== "");

      const kontakData = {
        name: document.getElementById("editKontakName")?.value.trim() || "",
        phone: document.getElementById("editKontakPhone")?.value.trim() || "",
        email: document.getElementById("editKontakEmail")?.value.trim() || "",
      };

      const formData = {
        id: currentEditCard?.dataset.id || "",
        kategori: document.getElementById("editKategori")?.value || "",
        nama: document.getElementById("editNamaKegiatan")?.value || "",
        deskripsi: document.getElementById("editDeskripsi")?.value || "",
        deadline: document.getElementById("editDeadline")?.value || "",
        peserta: document.getElementById("editPeserta")?.value || "",
        lokasi: document.getElementById("editLokasi")?.value || "",
        persyaratan: persyaratanValues,
        manfaat: manfaatValues,
        jadwal: document.getElementById("editJadwal")?.value || "",
        link: document.getElementById("editLink")?.value || "",
        kontak: kontakData,
      };

      if (!formData.kategori || !formData.nama) {
        alert("Kategori dan Nama Kegiatan harus diisi!");
        return;
      }

      try {
        const response = await fetch("/api/edit-activity", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (data.success) {
          closeEditModal();
          showSuccessModal("Data Kegiatan Berhasil Diperbarui!", "Perubahan telah disimpan ke sistem");
          setTimeout(() => {
            window.location.reload();
          }, 2000);
        } else {
          alert("Gagal memperbarui kegiatan: " + data.message);
        }
      } catch (error) {
        console.error("Error editing activity:", error);
        alert("Terjadi kesalahan saat memperbarui kegiatan.");
      }
    });
  }
}
function setupDeleteModal() {
  const deleteModal = document.getElementById("modalDeleteKegiatan");
  if (!deleteModal) return;

  const deleteButtons = document.querySelectorAll(".btn-delete");
  const nameLabel = document.getElementById("deleteKegiatanName");
  const cancelBtn = document.getElementById("btnCancelDelete");
  const confirmBtn = document.getElementById("btnConfirmDelete");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.stopPropagation(); // Prevent card click
      
      const card = this.closest(".kegiatan-card");
      deleteContext = {
        id: this.dataset.id || "",
        name: this.dataset.nama || card?.querySelector(".kegiatan-title")?.textContent || "Kegiatan",
      };

      if (nameLabel) {
        nameLabel.textContent = deleteContext.name || "Kegiatan";
      }

      openDeleteModal();
    });
  });

  if (cancelBtn) {
    cancelBtn.addEventListener("click", function (e) {
      e.preventDefault();
      closeDeleteModal();
    });
  }

  if (confirmBtn) {
    confirmBtn.addEventListener("click", async function (e) {
      e.preventDefault();

      if (!deleteContext.id) {
        alert("ID kegiatan tidak ditemukan");
        return;
      }

      try {
        const response = await fetch("/api/delete-activity", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: deleteContext.id }),
        });

        const data = await response.json();

        if (data.success) {
          closeDeleteModal();
          showSuccessModal("Kegiatan Berhasil Dihapus!", `${deleteContext.name} telah dihapus dari sistem`);
          setTimeout(() => {
            window.location.reload();
          }, 2000);
        } else {
          alert("Gagal menghapus kegiatan: " + data.message);
        }
      } catch (error) {
        console.error("Error deleting activity:", error);
        alert("Terjadi kesalahan saat menghapus kegiatan.");
      }
    });
  }
}

function setupCardNavigation() {
  const cards = document.querySelectorAll(".kegiatan-card");

  cards.forEach((card) => {
    const detailUrl = card.dataset.detailUrl;
    if (!detailUrl) return;

    card.addEventListener("click", function (e) {
      if (e.target.closest(".btn-edit") || e.target.closest(".btn-delete")) {
        return; // Do not navigate when clicking action buttons
      }
      window.location.href = detailUrl;
    });
  });
}

function setupAddActivityForm() {
  const btnUpload = document.getElementById("btnUploadKegiatan");

  // Setup multiple input functionality for Persyaratan
  const btnAddPersyaratan = document.getElementById("btnAddPersyaratan");
  if (btnAddPersyaratan) {
    btnAddPersyaratan.addEventListener("click", function () {
      addInputRow(
        "persyaratanContainer",
        "persyaratan[]",
        "Masukkan persyaratan kegiatan..."
      );
    });
  }

  // Setup multiple input functionality for Manfaat
  const btnAddManfaat = document.getElementById("btnAddManfaat");
  if (btnAddManfaat) {
    btnAddManfaat.addEventListener("click", function () {
      addInputRow(
        "manfaatContainer",
        "manfaat[]",
        "Masukkan manfaat & keuntungan kegiatan..."
      );
    });
  }

  if (btnUpload) {
  btnUpload.addEventListener("click", async function () {
    // Collect persyaratan
    const persyaratanInputs = document.querySelectorAll('input[name="persyaratan[]"]');
    const persyaratanValues = Array.from(persyaratanInputs)
      .map((input) => input.value.trim())
      .filter((value) => value !== "");

    // Collect manfaat
    const manfaatInputs = document.querySelectorAll('input[name="manfaat[]"]');
    const manfaatValues = Array.from(manfaatInputs)
      .map((input) => input.value.trim())
      .filter((value) => value !== "");

    // Collect contact info
    const kontakData = {
      name: document.getElementById("kontakName")?.value.trim() || "",
      phone: document.getElementById("kontakPhone")?.value.trim() || "",
      email: document.getElementById("kontakEmail")?.value.trim() || "",
    };

    // ✅ COLLECT CHECKED TRAITS
    const traitsCheckboxes = document.querySelectorAll('input[name="traits"]:checked');
    const selectedTraits = Array.from(traitsCheckboxes).map(cb => cb.value);

    const formData = {
      kategori: document.getElementById("kategori")?.value || "",
      nama: document.getElementById("namaKegiatan")?.value || "",
      deskripsi: document.getElementById("deskripsi")?.value || "",
      deadline: document.getElementById("deadline")?.value || "",
      peserta: document.getElementById("peserta")?.value || "",
      lokasi: document.getElementById("lokasi")?.value || "",
      persyaratan: persyaratanValues,
      manfaat: manfaatValues,
      jadwal: document.getElementById("jadwal")?.value || "",
      link: document.getElementById("link")?.value || "",
      kontak: kontakData,
      required_traits: selectedTraits.join(',')
    };

    // Validate
    if (!formData.kategori || !formData.nama) {
      alert("Kategori dan Nama Kegiatan harus diisi!");
      return;
    }

    if (selectedTraits.length === 0) {
      alert("Pilih minimal 1 trait kepribadian yang dibutuhkan!");
      return;
    }

    try {
      const response = await fetch("/api/add-activity", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.success) {
        closeModal();
        showSuccessModal("Kegiatan Berhasil Ditambahkan!", "Data kegiatan baru telah disimpan ke sistem");
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("Gagal menambahkan kegiatan: " + data.message);
      }
    } catch (error) {
      console.error("Error adding activity:", error);
      alert("Terjadi kesalahan saat menambahkan kegiatan.");
    }
  });
}
}

// Function to add new input row
function addInputRow(containerId, inputName, placeholder) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const inputRow = document.createElement("div");
  inputRow.className = "input-row";
  inputRow.innerHTML = `
        <input type="text" name="${inputName}" placeholder="${placeholder}" />
        <button type="button" class="btn-remove-input"><i class="bi bi-dash-lg"></i></button>
    `;

  container.appendChild(inputRow);

  // Add event listener to remove button
  const removeBtn = inputRow.querySelector(".btn-remove-input");
  removeBtn.addEventListener("click", function () {
    inputRow.remove();
  });

  // Focus the new input
  inputRow.querySelector("input").focus();
}

function setupFilterButtons() {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const kegiatanCards = document.querySelectorAll(".kegiatan-card");

  filterButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Remove active class from all buttons
      filterButtons.forEach((btn) => btn.classList.remove("active"));

      // Add active class to clicked button
      this.classList.add("active");

      // Get filter category
      let filterCategory = "";
      if (this.classList.contains("ukm")) filterCategory = "UKM";
      else if (this.classList.contains("organisasi"))
        filterCategory = "Organisasi";
      else if (this.classList.contains("kepanitiaan"))
        filterCategory = "Kepanitiaan";
      else if (this.classList.contains("lomba")) filterCategory = "Lomba";
      // 'semua' will have empty filterCategory

      // Filter cards
      kegiatanCards.forEach((card) => {
        if (filterCategory === "" || card.dataset.kategori === filterCategory) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
}

function filterKegiatan() {
  const searchInput = document.querySelector(".search-box input");
  const searchTerm = searchInput.value.toLowerCase();
  const kegiatanCards = document.querySelectorAll(".kegiatan-card");

  kegiatanCards.forEach((card) => {
    const title = card
      .querySelector(".kegiatan-title")
      .textContent.toLowerCase();
    const desc = card.querySelector(".kegiatan-desc").textContent.toLowerCase();

    if (title.includes(searchTerm) || desc.includes(searchTerm)) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
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

// Modal functions for adding kegiatan
function openModal() {
  const modal = document.getElementById("modalTambahKegiatan");
  if (modal) {
    // Reset all checkboxes
    const checkboxes = modal.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = false);
    
    // Reset other inputs
    const inputs = modal.querySelectorAll('input[type="text"], input[type="date"], input[type="url"], textarea, select');
    inputs.forEach(input => input.value = '');
    
    modal.classList.add("active");
  }
}

function closeModal() {
  const modal = document.getElementById("modalTambahKegiatan");
  if (modal) {
    modal.classList.remove("active");
  }
}

function openEditModal() {
  const modal = document.getElementById("modalEditKegiatan");
  if (modal) {
    modal.classList.add("active");
  }
}

function closeEditModal() {
  const modal = document.getElementById("modalEditKegiatan");
  if (modal) {
    modal.classList.remove("active");
  }
}

function openDeleteModal() {
  const modal = document.getElementById("modalDeleteKegiatan");
  if (modal) {
    modal.classList.add("active");
  }
}

function closeDeleteModal() {
  const modal = document.getElementById("modalDeleteKegiatan");
  if (modal) {
    modal.classList.remove("active");
  }
}

// Close modal when clicking outside
document.addEventListener("click", function (e) {
  const modal = document.getElementById("modalTambahKegiatan");
  if (e.target === modal) {
    closeModal();
  }

  const editModal = document.getElementById("modalEditKegiatan");
  if (e.target === editModal) {
    closeEditModal();
  }

  const deleteModal = document.getElementById("modalDeleteKegiatan");
  if (e.target === deleteModal) {
    closeDeleteModal();
  }
});

function fillEditModal(data) {
  setFieldValue("editKategori", data.kategori);
  setFieldValue("editNamaKegiatan", data.nama);
  setFieldValue("editDeskripsi", data.deskripsi);
  setFieldValue("editDeadline", data.deadline);
  setFieldValue("editPeserta", data.peserta);
  setFieldValue("editLokasi", data.lokasi);
  setFieldValue("editJadwal", data.jadwal);
  setFieldValue("editLink", data.link);
  setFieldValue("editKontakName", data.kontakName);
  setFieldValue("editKontakPhone", data.kontakPhone);
  setFieldValue("editKontakEmail", data.kontakEmail);

  resetInputGroup("editPersyaratanContainer", "");
  resetInputGroup("editManfaatContainer", "");
}

function setFieldValue(id, value) {
  const field = document.getElementById(id);
  if (!field) return;
  field.value = value || "";
}

// Success Modal Functions
function showSuccessModal(title, message) {
  const modal = document.getElementById("modalSuccess");
  const titleEl = document.getElementById("successTitle");
  const messageEl = document.getElementById("successMessage");
  
  if (titleEl) titleEl.textContent = title;
  if (messageEl) messageEl.textContent = message;
  
  if (modal) {
    modal.classList.add("active");
  }
}

function closeSuccessModal() {
  const modal = document.getElementById("modalSuccess");
  if (modal) {
    modal.classList.remove("active");
  }
}

function resetInputGroup(containerId, firstValue) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const rows = Array.from(container.querySelectorAll(".input-row"));
  rows.forEach((row, idx) => {
    if (idx === 0) {
      const input = row.querySelector("input");
      if (input) input.value = firstValue || "";
      row.querySelectorAll(".btn-remove-input").forEach((btn) => btn.remove());
    } else {
      row.remove();
    }
  });
}
