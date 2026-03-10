from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""
    patronymic = models.CharField('Patronymic', max_length=150, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def is_admin(self):
        """Проверка, является ли пользователь администратором"""
        return self.groups.filter(name='Admin').exists() or self.is_superuser

    @property
    def is_regular_user(self):
        """Проверка, является ли пользователь обычным пользователем"""
        return self.groups.filter(name='User').exists() and not self.is_admin