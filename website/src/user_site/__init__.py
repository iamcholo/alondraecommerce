import re
from django.conf import settings
from django.apps import apps as django_apps
from django.contrib.auth import load_backend
from django.middleware.csrf import rotate_token
from django.contrib.auth import REDIRECT_FIELD_NAME 
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from user_site.signals import user_site_logged_in, user_site_login_failed, user_site_logged_out
#from user_site.models import UserSite as User

SESSION_KEY = '_auth_user_site_id'
BACKEND_SESSION_KEY = '_auth_user_site_backend'
AUTH_USER_MODEL ='user_site.UserSite'

def login(request, user):
    if user is None:
        user = request.user_site
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.pk:
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.pk
    request.session[BACKEND_SESSION_KEY] = user.backend
    
    if hasattr(request, 'user_site'):
        request.user_site = user

    rotate_token(request)
    user_site_logged_in.send(sender=user.__class__, request=request, user_site=user)

def _clean_credentials(credentials):
    SENSITIVE_CREDENTIALS = re.compile('api|token|key|secret|password|signature', re.I)
    CLEANSED_SUBSTITUTE = '********************'
    for key in credentials:
        if SENSITIVE_CREDENTIALS.search(key):
            credentials[key] = CLEANSED_SUBSTITUTE
    return credentials


def get_backends():
    backends = []
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        
        if not backend_path in settings.EXCLUDE_AUTHENTICATION_BACKENDS:
            
            backends.append(load_backend(backend_path))
    if not backends:
        raise ImproperlyConfigured('No authentication backends have been defined. Does AUTHENTICATION_BACKENDS contain anything?')
    return backends


def authenticate(**credentials):
    
    for backend in get_backends():
        
        try:
            user = backend.authenticate(**credentials)
            
        except TypeError:           
            continue

        except PermissionDenied:
            return None

        if user is None:
            continue
        # Annotate the user object with the path of the backend.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    
        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_site_login_failed.send(sender=__name__,
            credentials=_clean_credentials(credentials))


def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user_site', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_site_logged_out.send(sender=user.__class__, request=request, user_site=user)

    # remember language choice saved to session
    language = request.session.get('django_language')
    if request.session.has_key(SESSION_KEY) and request.session.has_key(BACKEND_SESSION_KEY):
        del request.session[SESSION_KEY]
        del request.session[BACKEND_SESSION_KEY]
        request.session.modified = True
    #request.session.flush()

    if language is not None:
        request.session['django_language'] = language

    if hasattr(request, 'user_site'):
        from django.contrib.auth.models import AnonymousUser
        request.user_site = AnonymousUser()

def get_user_model():
    """
    Returns the User model that is active in this project.
    """
    if hasattr(settings, 'AUTH_USER_SITE_MODEL'):
        try:
            return django_apps.get_model(settings.AUTH_USER_MODEL)
        except ValueError:
            raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
        except LookupError:
            raise ImproperlyConfigured(
                "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
            )              
    else:            
        return User

def get_user(request):
    """
    Returns the user model instance associated with the given request session.
    If no user is retrieved an instance of `AnonymousUser` is returned.
    """
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