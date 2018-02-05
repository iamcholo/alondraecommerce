from django.conf.urls import include, url
from posts import rest_api as views 
from utilities.rest_api_urls import router 

register_url = True
urlpatterns = [
	url(r'^posts/{0,1}$', views.post_list),
	url(r'^post/{0,1}$', views.post),
	url(r'^post/details/{0,1}$', views.post_details),
	url(r'^pages/{0,1}$', views.post_list),
	url(r'^page/{0,1}$', views.post),
	url(r'^page/details/{0,1}$', views.post_details),
	url(r'^games/{0,1}$', views.post_list),
	url(r'^game/{0,1}$', views.post),
	url(r'^game/details/{0,1}$', views.post_details),
	url(r'^game_engines/{0,1}$', views.post_list),
	url(r'^game_engine/{0,1}$', views.post),
	url(r'^game_engine/details/{0,1}$', views.post_details),
	url(r'^videos/{0,1}$', views.post_list),
	url(r'^video/{0,1}$', views.post),
	url(r'^video/details/{0,1}$', views.post_details),
	url(r'^category/{0,1}$', views.category),
	url(r'^category/details/{0,1}$', views.category_details),
	url(r'^categories/{0,1}$', views.categories_list),
]






