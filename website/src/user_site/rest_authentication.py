from rest_framework.permissions import BasePermission
from rest_framework.compat import is_authenticated


class UserSiteIsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user_site and is_authenticated(request.user_site)
