from django.conf.urls import include, url
from globaly import rest_api as views 
from utilities.rest_api_urls import router 

register_url = True
urlpatterns = [
	url(r'^tags/{0,1}$', views.tag_list),
	url(r'^tag/{0,1}$', views.tag),
	url(r'^tag/details/{0,1}$', views.tag_details),
]





