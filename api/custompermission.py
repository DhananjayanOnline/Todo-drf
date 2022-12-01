from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):

    message="you have no permission"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user 