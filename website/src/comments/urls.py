from django.conf.urls import include, url
from comments import rest_api as views 
from utilities.rest_api_urls import router 

register_url = True
urlpatterns = [
	url(r'^comments/{0,1}$', views.comments),
	url(r'^comment/{0,1}$', views.comment),
	
]






