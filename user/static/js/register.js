// register.js - валидация формы регистрации

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const submitBtn = document.getElementById('submitBtn');
    const emailInput = document.getElementById('email');
    const nameInputs = ['last_name', 'first_name', 'patronymic'].map(id => document.getElementById(id));

    // Элементы для проверки пароля
    const strengthIndicator = document.getElementById('passwordStrength');
    const matchIndicator = document.getElementById('passwordMatch');
    const requirements = {
        length: document.getElementById('lengthReq'),
        uppercase: document.getElementById('uppercaseReq'),
        lowercase: document.getElementById('lowercaseReq'),
        number: document.getElementById('numberReq'),
        special: document.getElementById('specialReq')
    };

    // Проверка сложности пароля
    function checkPasswordStrength(password) {
        const checks = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };

        // Обновляем требования
        Object.keys(checks).forEach(key => {
            if (requirements[key]) {
                if (checks[key]) {
                    requirements[key].classList.add('valid');
                } else {
                    requirements[key].classList.remove('valid');
                }
            }
        });

        // Считаем количество выполненных требований
        const score = Object.values(checks).filter(Boolean).length;

        // Обновляем индикатор силы
        strengthIndicator.className = 'password-strength';
        if (password.length > 0) {
            if (score <= 2) {
                strengthIndicator.classList.add('weak');
            } else if (score <= 3) {
                strengthIndicator.classList.add('medium');
            } else {
                strengthIndicator.classList.add('strong');
            }
        }

        return checks;
    }

    // Проверка совпадения паролей
    function checkPasswordMatch() {
        const pass1 = password1.value;
        const pass2 = password2.value;

        if (pass2.length > 0) {
            if (pass1 === pass2) {
                matchIndicator.textContent = '✓ Пароли совпадают';
                matchIndicator.className = 'password-match match';
                return true;
            } else {
                matchIndicator.textContent = '✗ Пароли не совпадают';
                matchIndicator.className = 'password-match nomatch';
                return false;
            }
        } else {
            matchIndicator.textContent = '';
            return false;
        }
    }

    // Валидация email
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Валидация имени (только буквы и дефисы)
    function validateName(name) {
        const nameRegex = /^[A-Za-zА-Яа-я\-]+$/;
        return nameRegex.test(name);
    }

    // Форматирование имени (первая буква заглавная)
    function formatName(input) {
        input.addEventListener('input', function() {
            this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1).toLowerCase();
        });
    }

    // Применяем форматирование к полям имени
    nameInputs.forEach(input => {
        if (input) formatName(input);
    });

    // Проверка общей валидности формы
    function checkFormValidity() {
        const emailValid = validateEmail(emailInput.value);
        const namesValid = nameInputs.every(input => {
            if (input && input.hasAttribute('required')) {
                return input.value.length > 0 && validateName(input.value);
            }
            return true;
        });
        const passwordChecks = checkPasswordStrength(password1.value);
        const passwordsMatch = password2.value.length > 0 && password1.value === password2.value;

        const allValid = emailValid && namesValid &&
                        Object.values(passwordChecks).every(Boolean) &&
                        passwordsMatch;

        submitBtn.disabled = !allValid;
        return allValid;
    }

    // События для проверки пароля
    password1.addEventListener('input', function() {
        checkPasswordStrength(this.value);
        if (password2.value.length > 0) {
            checkPasswordMatch();
        }
        checkFormValidity();
    });

    password2.addEventListener('input', function() {
        checkPasswordMatch();
        checkFormValidity();
    });

    // События для email
    emailInput.addEventListener('input', function() {
        if (this.value.length > 0) {
            if (validateEmail(this.value)) {
                this.style.borderColor = '#22c55e';
            } else {
                this.style.borderColor = '#f97316';
            }
        } else {
            this.style.borderColor = '#e2e8f0';
        }
        checkFormValidity();
    });

    // События для полей имени
    nameInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    if (validateName(this.value)) {
                        this.style.borderColor = '#22c55e';
                    } else {
                        this.style.borderColor = '#f97316';
                    }
                } else {
                    this.style.borderColor = '#e2e8f0';
                }
                checkFormValidity();
            });
        }
    });

    // Отправка формы
    form.addEventListener('submit', function(e) {
        if (!checkFormValidity()) {
            e.preventDefault();

            // Показываем уведомление
            const notification = document.createElement('div');
            notification.className = 'notification-error';
            notification.textContent = 'Пожалуйста, исправьте ошибки в форме';
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 25px;
                background: #ef4444;
                color: white;
                border-radius: 12px;
                box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3);
                z-index: 9999;
                animation: slideInRight 0.3s ease;
            `;

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }, 3000);
        }
    });

    // Защита от случайного закрытия страницы
    let formChanged = false;

    form.addEventListener('input', function() {
        formChanged = true;
    });

    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = 'У вас есть незаполненные поля. Вы уверены, что хотите покинуть страницу?';
        }
    });

    // Добавляем анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});