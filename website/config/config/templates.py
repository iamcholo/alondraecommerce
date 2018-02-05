import os, sys
from django.conf import settings
DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(settings.BASE_DIR, 'public/html/admin/'),
            os.path.join(settings.BASE_DIR, 'public/html/default/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [        
                'django.template.context_processors.debug',
                'user.context_processors.user',
                'user_site.context_processors.user_site',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                 'sitemap.context_processors.get_domain',
                'django.template.context_processors.static',

            ],
        },
    },
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

DEFAUT_THEME = 'default'

MEDIA_URL = '/assets/media/'

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'public/content/media/')

MEDIA_UPLOAD_ROOT = os.path.join(settings.BASE_DIR, 'public/content/media/uploads/')

STATIC_URL = '/assets/'

ADMIN_STATIC_URL = '/admin/assets/'

PUBLIC_DIR = os.path.join(settings.BASE_DIR, 'public')

if DEBUG == False:
    STATIC_ROOT = os.path.join(settings.BASE_DIR, 'public/html/default/assets')
else:
    STATICFILES_DIRS = (
        os.path.join(settings.BASE_DIR, 'public/html/admin/assets/'),
        os.path.join(settings.BASE_DIR, 'public/html/default/assets/'),
        os.path.join(settings.BASE_DIR, 'public/content/media/uploads/'),
    )