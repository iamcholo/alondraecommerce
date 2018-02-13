from django.conf.urls import url
from comments import views 
# Create your views here.
urlpatterns = [

    url(r'^(?P<id>\d+)/{0,1}$',
        views.get_comments,     
        name='comments_get_comments'
    ),

	url(r'^(?P<id>\d+)/page/(?P<page>\d+)/{0,1}$',
        views.get_comments,
        name='comments_get_comments'
    ),

    url(r'^(?P<id>\d+)/ajax/{0,1}$',
        views.get_comments_ajax,     
        name='comments_get_comments_ajax'
    ),

	url(r'^(?P<id>\d+)/page/(?P<page>\d+)/ajax/{0,1}$',
        views.get_comments_ajax,
        name='comments_get_comments_ajax'
    ),

    url(r'^post/(?P<id>\d+)/ajax/{0,1}$',
        views.post_comment_ajax,     
        name='comments_post_comment_ajax'
    ),    
    
    url(r'^post/(?P<id>\d+)/(?P<parent>\d+)/ajax/{0,1}$',
        views.post_comment_ajax,     
        name='comments_post_comment_ajax'
    ),    

	url(r'^post/(?P<id>\d+)/{0,1}$',
        views.post_comment,
        name='comments_post_comment'
    ),

	url(r'^post/(?P<id>\d+)/(?P<parent>\d+)/{0,1}$',
        views.post_comment,
        name='comments_post_comment'
    ),

	url(r'^post/(?P<id>\d+)/(?P<post_id>\d+)/edit/ajax/{0,1}$',
        views.edit_post_comment_ajax,
        name='comments_edit_post_comment_ajax'
    ),

	url(r'^post/(?P<id>\d+)/(?P<post_id>\d+)/edit/{0,1}$',
        views.edit_post_comment,
        name='comments_edit_post_comment'
    ),
    
	url(r'^post/(?P<id>\d+)/(?P<post_id>\d+)/delete/ajax/{0,1}$',
        views.delete_post_comment_ajax,
        name='comments_delete_post_comment_ajax'
    ),

	url(r'^post/(?P<id>\d+)/(?P<post_id>\d+)/delete/{0,1}$',
        views.delete_post_comment,
        name='comments_delete_post_comment'
    ),

]