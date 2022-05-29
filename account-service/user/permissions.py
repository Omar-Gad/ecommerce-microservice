from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    
    
    def has_object_permission(self, request, view, obj):
        print(obj.id)
        print(request.user)
        return obj.id == request.user.id