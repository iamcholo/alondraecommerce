import user_site
from user_site.backends import UserSiteBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

def get_user(request):
    if not hasattr(request, '_cached_user_site'):
        request._cached_user_site = user_site.get_user(request)        
    return request._cached_user_site

class UserSiteAuthMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.user_site = SimpleLazyObject(lambda: get_user(request))

class RemoteUserSiteBackendMiddleware(object):

    header = "REMOTE_USER"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user_site'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'apps.user_site.middleware.UserSiteAuthMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            email = request.META[self.header]
        except KeyError:
            if request.user_site.is_authenticated():
                try:
                    stored_backend = user_site.load_backend(request.session.get(
                        user_site.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, UserSiteBackend):
                        user_site.logout(request)
                except ImproperlyConfigured as e:
                    # backend failed to load
                    user_site.logout(request)
            return

        if request.user_site.is_authenticated():
            if request.user_site.email == self.clean_username(email, request):
                return
        user = user_site.authenticate(remote_user=email)
        if user:
            request.user_site = user
            user_site.login(request, user)

    def clean_username(self, email, request):
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = user_site.load_backend(backend_str)
        try:
            username = backend.clean_username(email)
        except AttributeError:
            pass
        return username