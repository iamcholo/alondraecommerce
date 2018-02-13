from django.conf.urls import include, url
from discount import rest_api as views 
from utilities.rest_api_urls import router 
register_url = True
urlpatterns = [

	url(r'^discounts/{0,1}$', views.discounts_list),
	url(r'^discounts/create/{0,1}$', views.discounts_create),
	url(r'^discount/{0,1}$', views.discount),
	url(r'^discount/details/{0,1}$', views.discounts_details),
		




		
]






