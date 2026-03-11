from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """Форма регистрации нового пользователя"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        min_length=8
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(),
        min_length=8
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'last_name', 'first_name', 'patronymic')
        widgets = {
            'email': forms.EmailInput(),
            'last_name': forms.TextInput(),
            'first_name': forms.TextInput(),
            'patronymic': forms.TextInput(),
        }

    def clean_password2(self):
        """Проверка совпадения паролей"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        """Сохранение пользователя с зашифрованным паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """Форма обновления данных пользователя"""

    class Meta:
        model = CustomUser
        fields = ('email', 'last_name', 'first_name', 'patronymic')
        widgets = {
            'email': forms.EmailInput(),
            'last_name': forms.TextInput(),
            'first_name': forms.TextInput(),
            'patronymic': forms.TextInput(),
        }
