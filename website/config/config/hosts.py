SSL = False

if SSL == True:
    SESSION_COOKIE_SECURE = SSL
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
    CSRF_COOKIE_SECURE = SSL
    SECURE_SSL_REDIRECT = SSL


ALLOWED_HOSTS = [
 	'127.0.0.1',
    'localhost',
    'gamajuegos.com',
    'www.gamajuegos.com',
    '198.167.140.205',  
]
