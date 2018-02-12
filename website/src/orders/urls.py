from django.conf.urls import include, url
from rest_api import rest_api as views 
from utilities.rest_api_urls import router 
register_url = True
urlpatterns = [
	url(r'^orders/{0,1}$', views.order_list),
	url(r'^order/{0,1}$', views.order),
	url(r'^order/shipping/list/{0,1}$', views.order_shipping_item_list),
	url(r'^order/shipping/{0,1}$', views.order_shipping_item),	
]






