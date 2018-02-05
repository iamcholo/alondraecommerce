import os, sys
from django.conf import settings

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'es'

USE_TZ = False

LANGUAGES = (
    ('en', u'English'),
    ('es', u'Spanish'),
)

LOCALE_PATHS = [
    os.path.join(settings.BASE_DIR, 'config/locale/')
]