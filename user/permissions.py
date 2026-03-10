from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Разрешение только для администраторов"""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Admin').exists()
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешение: владелец объекта или админ"""

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Admin').exists():
            return True
        return obj == request.user