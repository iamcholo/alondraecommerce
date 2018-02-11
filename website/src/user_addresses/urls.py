from django.conf.urls import include, url
from taxes import rest_api as views 
from utilities.rest_api_urls import router 
register_url = True
urlpatterns = [

	url(r'^taxes/{0,1}$', views.address_list),
	url(r'^tax/{0,1}$', views.address),
	url(r'^tax/details/{0,1}$', views.address_details),
]






