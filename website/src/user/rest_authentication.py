from rest_framework.permissions import BasePermission
from rest_framework.compat import is_authenticated


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user)

class IsSuperUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return is_authenticated(request.user) and request.user.is_superuser 

