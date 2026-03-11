from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import Group

from .models import CustomUser
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
)
from .permissions import IsAdminUser, IsOwnerOrAdmin

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями
    GET /api/users/ - список пользователей (только админ)
    POST /api/users/ - создать пользователя (доступно всем)
    GET /api/users/{id}/ - детали пользователя (только админ или владелец)
    PUT/PATCH /api/users/{id}/ - обновить пользователя (только админ или владелец)
    DELETE /api/users/{id}/ - удалить пользователя (только админ)
    """
    queryset = CustomUser.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email', 'date_joined']
    ordering = ['id']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """Права доступа в зависимости от действия"""
        if self.action == 'create':
            # Регистрация доступна всем
            permission_classes = [AllowAny]
        elif self.action in ['list', 'destroy']:
            # Список и удаление только для админов
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Просмотр и редактирование для админа или владельца
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            # Остальное только для админов
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def set_admin(self, request, pk=None):
        """
        POST /api/users/{id}/set_admin/ - назначить администратора
        """
        user = self.get_object()
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        user.groups.add(admin_group)

        return Response({
            'success': True,
            'message': f'Пользователь {user.username} теперь администратор',
            'user': UserSerializer(user).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def remove_admin(self, request, pk=None):
        """
        POST /api/users/{id}/remove_admin/ - снять права администратора
        """
        user = self.get_object()
        admin_group = Group.objects.get(name='Admin')
        user.groups.remove(admin_group)

        return Response({
            'success': True,
            'message': f'У пользователя {user.username} сняты права администратора',
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        GET /api/users/me/ - информация о текущем пользователе
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def summary(self, request):
        """
        GET /api/users/summary/ - сводка о пользователе
        """
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name(),
            'is_admin': user.groups.filter(name='Admin').exists(),
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'groups': [group.name for group in user.groups.all()]
        })


class AuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet для авторизации
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        POST /api/auth/login/ - вход в систему
        """
        from django.contrib.auth import authenticate

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Необходимо указать username и пароль'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'message': 'Вход выполнен успешно',
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'error': 'Неверный username или пароль'
            }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        POST /api/auth/logout/ - выход из системы
        """
        if request.user.is_authenticated:
            logout(request)
            return Response({
                'success': True,
                'message': 'Выход выполнен успешно'
            })
        return Response({
            'error': 'Вы не авторизованы'
        }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def check(self, request):
        """
        GET /api/auth/check/ - проверка авторизации
        """
        if request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user': UserSerializer(request.user).data,
                'is_admin': request.user.groups.filter(name='Admin').exists()
            })
        else:
            return Response({
                'authenticated': False,
                'message': 'Пользователь не авторизован'
            }, status=status.HTTP_401_UNAUTHORIZED)
