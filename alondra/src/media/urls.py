from django.conf.urls import include, url
from media import rest_api as views 
from utilities.rest_api_urls import router 
register_url = True
urlpatterns = [
	url(r'^media/albums/{0,1}$', views.media_album_list),
	url(r'^media/album/{0,1}$', views.media_album),
	url(r'^media/album/create/{0,1}$', views.media_album_create),
	url(r'^images/{0,1}$', views.media_list),
	url(r'^image/create/{0,1}$', views.image_create),
	url(r'^image/{0,1}$', views.image),
	url(r'^image/details/{0,1}$', views.image_details),
		

		
]






