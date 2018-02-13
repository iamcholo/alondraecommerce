from navigation import rest_api as views 
from django.conf.urls import include, url
register_url = True
urlpatterns = [

    url(r'^navs/$', views.nav_list),
    url(r'^nav/$', views.nav_details),
    url(r'^nav/details/$', views.nav),
    url(r'^nav/items/$', views.nav_item_list),      	
 
]

