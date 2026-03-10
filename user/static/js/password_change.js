// password_change.js - валидация формы смены пароля

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('passwordForm');
    const newPass1 = document.getElementById('new_password1');
    const newPass2 = document.getElementById('new_password2');

    // Создаем индикатор сложности пароля
    const strengthIndicator = document.createElement('div');
    strengthIndicator.className = 'password-strength';
    newPass1.parentNode.appendChild(strengthIndicator);

    // Проверка сложности пароля
    newPass1.addEventListener('input', function() {
        const password = this.value;
        let strength = 'weak';

        if (password.length >= 8) {
            const hasUpperCase = /[A-Z]/.test(password);
            const hasLowerCase = /[a-z]/.test(password);
            const hasNumbers = /\d/.test(password);
            const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

            const score = [hasUpperCase, hasLowerCase, hasNumbers, hasSpecial].filter(Boolean).length;

            if (score >= 3 && password.length >= 10) {
                strength = 'strong';
            } else if (score >= 2) {
                strength = 'medium';
            }
        }

        strengthIndicator.className = 'password-strength ' + strength;
    });

    // Валидация формы
    form.addEventListener('submit', function(e) {
        const password = newPass1.value;
        const confirmPassword = newPass2.value;

        // Проверка длины пароля
        if (password.length < 8) {
            e.preventDefault();
            showError('Пароль должен быть минимум 8 символов!');
            highlightField(newPass1);
            return;
        }

        // Проверка совпадения паролей
        if (password !== confirmPassword) {
            e.preventDefault();
            showError('Новые пароли не совпадают!');
            highlightField(newPass2);
            return;
        }

        // Дополнительная проверка на простые пароли
        const commonPasswords = ['password', '12345678', 'qwerty123', 'admin123'];
        if (commonPasswords.includes(password.toLowerCase())) {
            e.preventDefault();
            showError('Этот пароль слишком простой. Придумайте более сложный пароль!');
            highlightField(newPass1);
            return;
        }
    });

    // Функция подсветки поля с ошибкой
    function highlightField(field) {
        field.classList.add('error');
        setTimeout(() => {
            field.classList.remove('error');
        }, 2000);
    }

    // Функция показа ошибки
    function showError(message) {
        // Проверяем, есть ли уже блок с ошибкой
        let errorDiv = document.querySelector('.error-message');

        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            form.insertBefore(errorDiv, form.firstChild);
        }

        errorDiv.textContent = message;
        errorDiv.style.display = 'block';

        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 3000);
    }
});