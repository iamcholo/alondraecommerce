from django.conf.urls import include, url
import rest_api as views 
register_url = True
urlpatterns = [
    url(r'^cart/add/{0,1}$', views.add_to_cart, name="payment_add_to_cart"),
    url(r'^cart/items/length/{0,1}$', views.count_cart_elements, name="count_cart_elements"),
]






