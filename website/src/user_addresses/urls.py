from django.conf.urls import include, url
from user_addresses import rest_api as views 
from utilities.rest_api_urls import router 

register_url = True
urlpatterns = [

	url(r'^address/list/{0,1}$', views.address_list),
	url(r'^address/{0,1}$', views.address),
	url(r'^address/details/{0,1}$', views.address_details),
]






