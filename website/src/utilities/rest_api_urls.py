#encoding:utf-8
import importlib
import os, sys
from rest_framework.routers import DefaultRouter
from django.conf.urls import  include, url
router = DefaultRouter()
from django.conf import settings
apiurls =  []
base_auth_url = "auth"
if (hasattr(settings, 'BASE_AUTH_URL')):
	base_auth_url = settings.BASE_AUTH_URL 
for i,a in enumerate(settings.INSTALLED_APPS):
	app_dir = os.path.join(settings.SOURCE_DIR, a.replace('.','/'))
	app_urls = os.path.join(settings.SOURCE_DIR, a.replace('.','/') ) + '/urls.py'
	urls =  a + '.urls'

	if(os.path.isdir(app_dir) == True and os.path.exists(app_urls) == True):
		module = importlib.import_module(urls)
		
		if hasattr(module, 'register_url') and hasattr(module, 'urlpatterns'):
			if (hasattr(module, base_auth_url) and module.auth==True ):
				apiurls +=  url(r'^%s/' % base_auth_url , include(urls)),
			else:
				apiurls += module.urlpatterns


   
