from rest_framework import permissions

class AppOwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user.applicant == obj


class AppIsAuthenticated(permissions.IsAuthenticated):
        def has_permission(self, request, view):
            return bool(request.user.applicant and request.user.is_authenticated)


class EmOwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user.employer == obj


class EmIsAuthenticated(permissions.IsAuthenticated):
        def has_permission(self, request, view):
            return bool(request.user.employer and request.user.is_authenticated)
