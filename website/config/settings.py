import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(1,os.path.join(BASE_DIR, 'src')) 
from django.conf import settings

try:
    from config.local_settings import *
    from config.apis import *
    from config.applications import *
    from config.celery import *
    from config.databases import *
    from config.email import *
    from config.hosts import *    
    from config.locales import *
    from config.middleware import *
    from config.templates import *
    from config.vendor_apps import *
except ImportError:
    pass

