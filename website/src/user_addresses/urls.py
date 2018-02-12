from django.conf.urls import include, url
from taxes import rest_api as views 
from user_addresses.rest_api_urls import router 
register_url = True
urlpatterns = [

	url(r'^address/list/{0,1}$', views.address_list),
	url(r'^address/{0,1}$', views.address),
	url(r'^address/details/{0,1}$', views.address_details),
]






