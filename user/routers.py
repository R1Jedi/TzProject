from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')
