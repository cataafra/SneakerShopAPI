from rest_framework import permissions

from api.models import UserProfile


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.profile.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.profile.role == 'admin')

class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.profile.role in ['admin', 'moderator']


class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.profile.role in ['admin', 'moderator', 'regular']


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

        if request.method in SAFE_METHODS:
            return True

        if UserProfile.objects.filter(user=request.user).exists():
            user_profile = UserProfile.objects.get(user=request.user)

            return (
                    request.user == obj.created_by or user_profile.role in ['admin', 'moderator']
            )

        return False