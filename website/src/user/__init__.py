import re
from django.conf import settings
from django.contrib.auth import load_backend
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'


def get_user(request):
    from django.contrib.auth.models import AnonymousUser
    try:
        user_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
        assert backend_path in settings.AUTHENTICATION_BACKENDS
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
    except (KeyError, AssertionError):
        user = AnonymousUser()
    return user