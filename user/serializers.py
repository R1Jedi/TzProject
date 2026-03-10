from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""
    full_name = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'patronymic', 'full_name', 'is_active', 'is_admin',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_admin(self, obj):
        return obj.groups.filter(name='Admin').exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'patronymic']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)

        # Добавляем в группу User
        user_group, _ = Group.objects.get_or_create(name='User')
        user.groups.add(user_group)

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления пользователя"""

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic']

    def validate_username(self, value):
        if self.instance and self.instance.username == value:
            return value
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким username уже существует')
        return value

    def validate_email(self, value):
        if self.instance and self.instance.email == value:
            return value
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        return value


class SetAdminSerializer(serializers.Serializer):
    """Сериализатор для назначения администратора"""
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            self.user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return value

    def save(self):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.user.groups.add(admin_group)
        return self.user


class RemoveAdminSerializer(serializers.Serializer):
    """Сериализатор для снятия прав администратора"""
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            self.user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return value

    def save(self):
        admin_group = Group.objects.get(name='Admin')
        self.user.groups.remove(admin_group)
        return self.user