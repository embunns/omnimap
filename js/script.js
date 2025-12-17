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
});
