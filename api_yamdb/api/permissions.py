from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from users.models import User


class IsAdmin(BasePermission):
    """Разрешение для управления пользоватклями."""

    def has_permission(self, request: Request, view: None) -> bool:
        return request.user.is_authenticated and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )

    def has_object_permission(self, request: Request, view: None, obj) -> bool:
        return request.user.is_superuser or request.user.role == User.ADMIN


class IsAdminOrReadOnly(BasePermission):
    """Разрешение редактирования только Админу."""

    def has_permission(self, request: Request, view: None) -> bool:
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.role == User.ADMIN or request.user.is_superuser)
        )


class IsUserAdminAuthorModeratorOrReadOnly(BasePermission):
    """Разрешение редактирования только Админу, Автору и Модератору."""

    def has_permission(self, request: Request, view: None) -> bool:
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request: Request, view: None, obj) -> bool:
        return request.method in SAFE_METHODS or (
            obj.author == request.user
            or request.user.role == User.MODERATOR
            or request.user.role == User.ADMIN
            or request.user.is_superuser
        )
