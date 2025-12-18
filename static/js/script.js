document.addEventListener("DOMContentLoaded", () => {

    /* =======================
       SHOW / HIDE PASSWORD
    ======================== */
    const togglePassword = document.getElementById("tooglePassword");
    const passwordInput = document.getElementById("password");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", () => {
            const type =
                passwordInput.getAttribute("type") === "password"
                    ? "text"
                    : "password";

            passwordInput.setAttribute("type", type);
            togglePassword.classList.toggle("bi-eye");
            togglePassword.classList.toggle("bi-eye-slash");
        });
    }

    /* =======================
       PASSWORD VALIDATION
    ======================== */
    const passwordError = document.getElementById("passwordError");
    const loginBtn = document.getElementById("btn-login");

    if (loginBtn && passwordInput) {
        loginBtn.addEventListener("click", e => {
            e.preventDefault();

            passwordError.classList.add("d-none");
            passwordInput.classList.remove("is-invalid");

            if (passwordInput.value.trim() === "") {
                passwordError.classList.remove("d-none");
                passwordInput.classList.add("is-invalid");
                return;
            }

            // MODAL SUCCESS
            const modalEl = document.getElementById("loginSuccessModal");
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();

                setTimeout(() => {
                    window.location.href = "dashboard.html";
                }, 2000);
            }
        });

        passwordInput.addEventListener("input", () => {
            if (passwordInput.value.trim() !== "") {
                passwordError.classList.add("d-none");
                passwordInput.classList.remove("is-invalid");
            }
        });
    }

    /* =======================
       SIDEBAR DROPDOWN
    ======================== */
    const sidebar = document.getElementById("sidebar");
    const allDropdown = document.querySelectorAll("#sidebar .side-dropdown");

    allDropdown.forEach(dropdown => {
        const trigger = dropdown.parentElement.querySelector("a:first-child");

        trigger.addEventListener("click", e => {
            e.preventDefault();

            allDropdown.forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove("show");
                    d.parentElement
                        .querySelector("a:first-child")
                        .classList.remove("active");
                }
            });

            trigger.classList.toggle("active");
            dropdown.classList.toggle("show");
        });
    });

    /* =======================
       SIDEBAR COLLAPSE (FIXED)
    ======================== */
    const toggleSidebar = document.querySelector("nav .toggle-sidebar");

    if (toggleSidebar && sidebar) {
        toggleSidebar.addEventListener("click", () => {
            sidebar.classList.toggle("hide");

            allDropdown.forEach(item => {
                item.classList.remove("show");
                item.parentElement
                    .querySelector("a:first-child")
                    .classList.remove("active");
            });
        });
    }

    const btnMulaiTes = document.getElementById("btn-start-test");
    const introContent = document.getElementById("introContent");
    const questionContent = document.getElementById("questionContent");
    const tesWrapper = document.getElementById("test-wrapper");
    const btnNext = document.getElementById("btnNextTest");
    const btnFinish = document.getElementById("btnFintest");
    const quest = document.querySelector(".quest");
    const finishQuest = document.querySelector(".fin-quest");
    const answerButtons = document.querySelectorAll(".tes-answer-btn");
    const ConfirmTestModal = document.getElementById("ConfirmTestModal");
    const finishTestModal = document.getElementById("FinishTestModal");

    let selectedAnswer = null;

    // Mulai Tes
    if (btnMulaiTes && introContent && questionContent && tesWrapper) {
        btnMulaiTes.addEventListener("click", () => {
            introContent.classList.add("d-none");
            questionContent.classList.remove("d-none");
            tesWrapper.classList.add("no-paper");
        });
    }

    // Pilih Jawaban
    answerButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Reset active class dari semua tombol
            answerButtons.forEach(b => b.classList.remove("active"));

            // Set active ke tombol yang diklik
            btn.classList.add("active");
            selectedAnswer = btn.dataset.value;
            console.log("Jawaban dipilih:", selectedAnswer);
        });
    });

    //  HELPER: Fungsi Validasi & Submit untuk
    //  mengecek apakah user sudah memilih jawaban
    const validateAndGetAnswer = () => {
        if (!selectedAnswer) {
            alert("Pilih jawaban terlebih dahulu!");
            return false;
        }

        console.log("Submit jawaban ke sistem:", selectedAnswer);

        // Bisa ditaroh logika post data ke backend

        return true;
    };

    // HELPER: Reset Selection untuk membersihkan pilihan setelah klik next
    const resetSelection = () => {
        selectedAnswer = null;
        answerButtons.forEach(b => b.classList.remove("active"));
    };

    // Tombol NEXT yg hanya bisa lanjut hanya jika sudah menjawab
    if (btnNext) {
        btnNext.addEventListener("click", () => {
            // Cek validasi dulu
            if (validateAndGetAnswer()) {
                quest.classList.add("d-none");
                finishQuest.classList.remove("d-none");

                // Opsional: Reset jawaban jika 'finishQuest' adalah pertanyaan baru
                resetSelection();
            }
        });
    }

    // Tombol FINISH hanya jika sudah menjawab dan munculkan Modal
    if (btnFinish) {
        btnFinish.addEventListener("click", () => {
            // Cek validasi dulu (karena user minta finish juga harus validasi jawaban terakhir)
            if (validateAndGetAnswer()) {
                // Tampilkan Modal Konfirmasi
                const modal = new bootstrap.Modal(ConfirmTestModal);
                modal.show();
            }
        });
    }

    if (finishTestModal) {
        const modal = new bootstrap.Modal(finishTestModal);
        
        finishTestModal.addEventListener('show.bs.modal', function () {
            setTimeout(() => {
                modal.hide();
                window.location.href = "dashboard.html";
            }, 2000);
        });
    }

    /* =======================
       DASHBOARD CHARTS
    ======================== */
    initializeDashboardCharts();

});

// Initialize all dashboard charts
function initializeDashboardCharts() {
    // Wait a bit to ensure Chart.js is fully loaded
    setTimeout(() => {
        // Check if Chart.js is loaded
        if (typeof Chart === 'undefined') {
            console.warn('Chart.js is not loaded');
            return;
        }
        
        initializeCharts();
    }, 100);
}

function initializeCharts() {

    // Kategori Kegiatan Donut Chart
    const kategoriCtx = document.getElementById('kategoriKegiatanChart');
    if (kategoriCtx) {
        const kategoriChart = new Chart(kategoriCtx, {
            type: 'doughnut',
            data: {
                labels: ['Kepanitiaan', 'UKM', 'Organisasi'],
                datasets: [{
                    data: [64, 43, 5],
                    backgroundColor: ['#e91e63', '#64b5f6', '#ff9800'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '%';
                            }
                        }
                    }
                }
            }
        });
        console.log('Kategori Kegiatan chart initialized');
    }

    // Skor Rata-rata Gauge Chart (semi-circle)
    const gaugeCtx = document.getElementById('skorRataRataGauge');
    if (gaugeCtx) {
        const gaugeChart = new Chart(gaugeCtx, {
            type: 'doughnut',
            data: {
                labels: ['Skor', 'Sisa'],
                datasets: [{
                    data: [72, 28],
                    backgroundColor: ['#2196f3', '#e0e0e0'],
                    borderWidth: 0,
                    cutout: '75%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                circumference: 180,
                rotation: -90,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            }
        });
        console.log('Skor Rata-rata gauge chart initialized');
    }

    // Bar Chart for "Waktu kamu sering dihabisin buat..."
    const barCtx = document.getElementById('omniUniqueBarChart');
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['Belajar', 'Organisasi', 'UKM', 'Hobi', 'Lainnya'],
                datasets: [{
                    label: 'Jam per Minggu',
                    data: [25, 15, 10, 8, 5],
                    backgroundColor: '#c62828',
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' jam/minggu';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 5
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    
    /* =======================
       LOGOUT HANDLER
    ======================== */
    const confirmLogout = document.getElementById("confirmLogout");
    if (confirmLogout) {
        confirmLogout.addEventListener("click", () => {
            console.log("Logout clicked");
            
            fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Logout response:", data);
                if (data.success) {
                    window.location.href = '/login';
                }
            })
            .catch(error => {
                console.error('Logout error:', error);
                // Still redirect to login even on error
                window.location.href = '/login';
            });
        });
    }

});