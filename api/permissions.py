from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.profile.role == 'admin')

class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.profile.role in ['admin', 'moderator'])


class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.profile.role in ['admin', 'moderator', 'regular'])

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.created_by)