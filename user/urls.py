from django.urls import path, include
from . import views
from .routers import router

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('password-change/', views.password_change_view, name='password_change'),

    path('delete-account/', views.account_delete_view, name='account_delete'),

    path('api/', include(router.urls)),
]
