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
    btnMulaiTes.addEventListener("click", () => {
        introContent.classList.add("d-none");
        questionContent.classList.remove("d-none");
        tesWrapper.classList.add("no-paper");
    });

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

});
