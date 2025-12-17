//show password
 // Ambil elemen DOM
 const tooglePassword = document.querySelector('#tooglePassword');
 const password = document.querySelector('#password');

 // Tambahkan event listener untuk ikon
 tooglePassword.addEventListener('click', () => {
     // Ubah tipe input antara 'password' dan 'text'
     const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
     password.setAttribute('type', type);

     // Ubah ikon mata
     tooglePassword.classList.toggle('bi-eye');
     tooglePassword.classList.toggle('bi-eye-slash');
 });

document.addEventListener("DOMContentLoaded", () => {
    const password = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const loginBtn = document.getElementById("btn-login");

    if (!loginBtn) return; // safety check

    loginBtn.addEventListener("click", (e) => {
        e.preventDefault();

        // reset error
        passwordError.classList.add("d-none");
        password.classList.remove("is-invalid");

        // cek password kosong
        if (password.value.trim() === "") {
            passwordError.classList.remove("d-none");
            password.classList.add("is-invalid");
            return;
        }
    });

    //delete warning when typing
    password.addEventListener("input", () => {
        if (password.value.trim() !== "") {
            passwordError.classList.add("d-none");
            password.classList.remove("is-invalid");
        }
    });
});

//modal login success and redirect to dashboard
document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.getElementById("btn-login");

    loginBtn.addEventListener("click", (e) => {
        e.preventDefault();

        // tampilkan modal
        const modal = new bootstrap.Modal(
            document.getElementById("loginSuccessModal")
        );
        modal.show();

        // redirect setelah 2 detik
        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 2000);
    });
});
