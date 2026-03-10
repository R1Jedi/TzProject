// profile.js - скрипты для страницы профиля

document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');
    let formChanged = false;
    let originalFormData = new FormData(profileForm);

    // Функция для сравнения данных формы
    function hasFormChanged() {
        const currentFormData = new FormData(profileForm);
        for (let [key, value] of currentFormData.entries()) {
            if (value !== originalFormData.get(key)) {
                return true;
            }
        }
        return false;
    }

    // Отслеживание изменений в форме
    profileForm.addEventListener('input', function() {
        formChanged = hasFormChanged();
    });

    profileForm.addEventListener('change', function() {
        formChanged = hasFormChanged();
    });

    // Сброс флага при отправке формы
    profileForm.addEventListener('submit', function(e) {
        formChanged = false;

        // Дополнительная валидация перед отправкой
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;

        if (!validateUsername(username)) {
            e.preventDefault();
            showNotification('Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_', 'error');
            return;
        }

        if (!validateEmail(email)) {
            e.preventDefault();
            showNotification('Пожалуйста, введите корректный email адрес', 'error');
            return;
        }
    });

    // Предупреждение при попытке покинуть страницу с несохраненными изменениями
    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = 'У вас есть несохраненные изменения. Вы уверены, что хотите покинуть страницу?';
            return e.returnValue;
        }
    });

    // Валидация имени пользователя
    function validateUsername(username) {
        const usernameRegex = /^[\w.@+-]+$/;
        return usernameRegex.test(username) && username.length > 0;
    }

    // Валидация email
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Показ уведомлений
    function showNotification(message, type) {
        // Создаем элемент уведомления
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${type === 'error' ? '#ef4444' : '#22c55e'};
            color: white;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Удаляем уведомление через 3 секунды
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Добавляем анимации для уведомлений
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
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

    // Подсветка полей при ошибках
    function highlightField(field) {
        field.classList.add('error');
        setTimeout(() => {
            field.classList.remove('error');
        }, 2000);
    }

    // Дополнительная проверка при потере фокуса с полей
    const usernameField = document.getElementById('username');
    const emailField = document.getElementById('email');

    usernameField.addEventListener('blur', function() {
        if (!validateUsername(this.value)) {
            highlightField(this);
            showNotification('Некорректное имя пользователя', 'error');
        }
    });

    emailField.addEventListener('blur', function() {
        if (!validateEmail(this.value)) {
            highlightField(this);
            showNotification('Некорректный email адрес', 'error');
        }
    });

    // Автоматическое форматирование полей
    const nameFields = ['first_name', 'last_name', 'patronymic'];
    nameFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', function() {
                // Первая буква заглавная, остальные строчные
                this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1).toLowerCase();
            });
        }
    });
});