from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
import views as  views

urlpatterns = patterns('',
        url(r'^add/(?P<product_id>\d+)/{0,1}$',
                views.add_to_cart,
                name='cart_add_to_cart'
        ),
        url(r'^add/(?P<product_id>\d+)/(?P<variation>\d+)/{0,1}$',
                views.add_to_cart,
                name='cart_add_to_cart'
        ),

        url(r'^remove/(?P<product_id>\d+)/{0,1}$',
                views.remove_from_cart,
                name='cart_remove_from_cart'
        ),

        url(r'^/{0,1}$',
                views.get_cart,
                name='get_cart'
        ),

        url(r'^cart/clear/{0,1}$',
                views.clear_cart,
                name='cart_clear_cart'
        ),






)