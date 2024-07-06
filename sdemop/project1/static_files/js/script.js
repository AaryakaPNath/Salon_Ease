const showPasswordIcon = document.getElementById('show-password');
const passwordInput = document.getElementById('password');

showPasswordIcon.addEventListener('click', function() {
  // Toggle password type between "password" and "text"
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    showPasswordIcon.classList.remove('fa-eye-slash');
    showPasswordIcon.classList.add('fa-eye'); // Change icon to "show password"
  } else {
    passwordInput.type = 'password';
    showPasswordIcon.classList.remove('fa-eye');
    showPasswordIcon.classList.add('fa-eye-slash'); // Change icon back to "hide password"
  }
});
