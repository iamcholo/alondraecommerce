from django.conf.urls import include, url
from payments import rest_api as views 
from utilities.rest_api_urls import router 
register_url = True
urlpatterns = [
	url(r'^payments/{0,1}$', views.payment_list),
	url(r'^payment/{0,1}$', views.payment),
	url(r'^payment/details/{0,1}$', views.payment_create),
]






