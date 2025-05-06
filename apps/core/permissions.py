from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True

        if hasattr(obj, "booked_by"):
            return obj.booked_by == request.user or request.user.is_staff
        elif hasattr(obj, "user"):
            return obj.user == request.user or request.user.is_staff
        return request.user.is_staff
