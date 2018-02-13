
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_PERMISSION_CLASSES': (
          'rest_framework.permissions.IsAuthenticated',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
    '127.0.0.1:8000',

    'localhost',
    'webdisenoya.com',
    'projects.webdisenoya.com',
    '198.167.140.205',   
)
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'X_USERNAME',
    'X_PASSWORD',
    'HTTP_X_USERNAME',
    'HTTP_X_PASSWORD',
    'WWW-Authenticate',
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)



#
AUTH_USER_MODEL = 'user.CustomUser'

RECAPTCHA_PUBLIC_KEY = '6LdB3RMTAAAAAI8KOCSQFrS9PnSim4H-d7mDQq99'
RECAPTCHA_PRIVATE_KEY = '6LdB3RMTAAAAAGzpNezah55TZwtOqCSApJJ_bcDy'
#CAPTCHA_AJAX = True
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True