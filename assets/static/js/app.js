document.getElementById('password-eye').addEventListener('click', () => {
    const passwordInput = document.getElementById('password');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
});

document.getElementById('confirm-password-eye').addEventListener('click', () => {
    const confirmPasswordInput = document.getElementById('confirm-password');
    if (confirmPasswordInput.type === 'password') {
        confirmPasswordInput.type = 'text';
    } else {
        confirmPasswordInput.type = 'password';
    }
});

document.getElementById('confirm-password').addEventListener('input', () => {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        document.getElementById('error-message').innerText = '**Passwords do not match';
    } else {
        document.getElementById('error-message').innerText = '';
    }
});