from rest_framework import permissions


class IsAdminModAuthorOrReading(permissions.BasePermission):
    '''Ограничения прав доступа к моделям Review, Comment.'''

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_moderator_or_admin
        )


class IsAdminOrReading(permissions.BasePermission):
    '''Ограничения прав доступа к моделям Genre, Category, Title.'''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    '''Ограничения прав доступа к модели User.'''

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )
