from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser


def index(request):
    """Главная страница"""
    return render(request, 'index.html')


def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        # Простая валидация
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic', '')

        # Проверки
        errors = []
        if password1 != password2:
            errors.append('Пароли не совпадают')
        if len(password1) < 8:
            errors.append('Пароль должен быть минимум 8 символов')

        from .models import CustomUser
        if CustomUser.objects.filter(email=email).exists():
            errors.append('Пользователь с таким email уже существует')
        if CustomUser.objects.filter(username=username).exists():
            errors.append('Пользователь с таким именем уже существует')

        if not errors:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                last_name=last_name,
                first_name=first_name,
                patronymic=patronymic
            )
            login(request, user)
            messages.success(request, '✅ Регистрация прошла успешно!')
            return redirect('profile')
        else:
            for error in errors:
                messages.error(request, error)

    return render(request, 'register.html')


def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'👋 С возвращением, {user.first_name}!')
                return redirect('profile')
            else:
                messages.error(request, 'Ваш аккаунт деактивирован')
        else:
            messages.error(request, 'Неверный username или пароль')

    return render(request, 'login.html')


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, '👋 Вы вышли из системы')
    return redirect('login')


@login_required
def profile_view(request):
    """Просмотр и редактирование профиля"""
    if request.method == 'POST':
        user = request.user

        # Получаем данные из формы
        new_username = request.POST.get('username', '').strip()
        new_email = request.POST.get('email', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        # Список ошибок
        errors = []

        if not new_username:
            errors.append('Username не может быть пустым')
        if not new_email:
            errors.append('Email не может быть пустым')

        if new_username and new_username != user.username:
            if CustomUser.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                errors.append(f'Пользователь с username "{new_username}" уже существует')

        if new_email and new_email != user.email:
            if CustomUser.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                errors.append(f'Пользователь с email "{new_email}" уже существует')

        if errors:
            for error in errors:
                messages.error(request, error)

            # Возвращаем пользователя на страницу с сохранением введенных данных
            return render(request, 'profile.html', {
                'user': user,
                'form_data': {
                    'username': new_username,
                    'email': new_email,
                    'last_name': last_name,
                    'first_name': first_name,
                    'patronymic': patronymic
                }
            })

        user.username = new_username
        user.email = new_email
        user.last_name = last_name
        user.first_name = first_name
        user.patronymic = patronymic
        user.save()

        messages.success(request, '✅ Профиль успешно обновлен!')
        return redirect('profile')

    return render(request, 'profile.html', {'user': request.user})


@login_required
def password_change_view(request):
    """Смена пароля"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        # Проверки
        if not user.check_password(old_password):
            messages.error(request, 'Неверный текущий пароль')
        elif new_password1 != new_password2:
            messages.error(request, 'Новые пароли не совпадают')
        elif len(new_password1) < 8:
            messages.error(request, 'Пароль должен быть минимум 8 символов')
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, '✅ Пароль успешно изменен!')
            return redirect('profile')

    return render(request, 'password_change.html')


@login_required
def account_delete_view(request):
    """Мягкое удаление аккаунта"""
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=request.user.username, password=password)

        if user is not None:
            user.is_active = False
            user.save()
            logout(request)
            messages.success(request, 'Ваш аккаунт деактивирован')
            return redirect('login')
        else:
            messages.error(request, 'Неверный пароль')

    return render(request, 'account_delete_confirm.html')
