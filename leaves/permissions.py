from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Доступ только для администраторов (отдел кадров)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOwn(BasePermission):
    """Admin — полный доступ. Employee — только свои данные."""
    def has_permission(self, request, view):
        return request.user.is_authenticated
