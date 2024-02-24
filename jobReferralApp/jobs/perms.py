from rest_framework import permissions

class EmOwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user.employer == obj.employer

class EmIsAuthenticated(permissions.IsAuthenticated):
        def has_permission(self, request, view):
            return bool(request.user.employer and request.user.is_authenticated)


class AppIsAuthenticated(permissions.IsAuthenticated):
        def has_permission(self, request, view):
            return bool(request.user.applicant and request.user.is_authenticated)



