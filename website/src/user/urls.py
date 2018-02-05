from user import rest_api as views 
from django.conf.urls import include, url
register_url = True
urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^check/online/$', views.check_online),
    url(r'^logout/$', views.logout),
    url(r'^users/$', views.user_list),
    url(r'^user/$', views.user_details),
    url(r'^user/delete/$', views.delete_user),    
    url(r'^new/user/$', views.user_create),
  	url(r'^me/$', views.user),
  	url(r'^me/password/$', views.user_udpate_password),	
]
