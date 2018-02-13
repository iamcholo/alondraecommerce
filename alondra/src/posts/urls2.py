
from django.conf.urls import url
from posts import views 
# Create your views here.
urlpatterns = [
    
    #url(r'^$',
    #        views.home,
    #        name='blog_home'
    #        ),
    #    
    #url(r'^page/(?P<page>\d+)/{0,1}$',
    #        views.home,
    #        name='blog_home'),
    #
    url(r'^category/(?P<slug>[0-9A-Za-z-_]+)/{0,1}$',
            views.category,
            name='category'
        ),

    url(r'^games/{0,1}$',
            views.games,
            name='games'
        ),

    url(r'^games/page/(?P<page>\d+)/{0,1}$',
            views.games,
            name='games'
        ),
    url(r'^videos/{0,1}$',
            views.videos,
            name='videos'
        ),

    url(r'^videos/page/(?P<page>\d+)/{0,1}$',
            views.videos,
            name='videos'
        ),

    url(r'^game-engines/{0,1}$',
            views.games_engines,
            name='games_engines'
        ),

    url(r'^game-engines/page/(?P<page>\d+)/{0,1}$',
            views.games_engines,
            name='games_engines'
        ),

    url(r'^search/{0,1}$',
            views.search,
            name='search'
        ),

    url(r'^search/page/(?P<page>\d+)/{0,1}$',
            views.search,
            name='search'
        ),

    #url(r'^(?P<slug>[0-9A-Za-z-_]+)/page/(?P<page>\d+)/{0,1}$',
    #        views.category,
    #        name='category'
    #    ),
    #
    #url(r'^(?P<slug>[0-9A-Za-z-_]+)/{0,1}$',
    #       views.post_details,
    #       name='post_details'
    #    ),
    
    url(r'^autor/(?P<slug>[0-9A-Za-z-_]+)/page/(?P<page>\d+)/{0,1}$',
        views.autor,
        name='posts_autor'
    ),

    url(r'^autor/(?P<slug>[0-9A-Za-z-_]+)/{0,1}$',
           views.autor,
           name='posts_autor'
    ),
    
    url(r'^tag/(?P<slug>[0-9A-Za-z-_]+)/page/(?P<page>\d+)/{0,1}$',
        views.tags,
        name='posts_tags'
    ),

    url(r'^tag/(?P<slug>[0-9A-Za-z-_]+)/{0,1}$',
           views.tags,
           name='posts_tags'
    ),

    url(r'^(?P<slug>[0-9A-Za-z-_]+)/(?P<sub_slug>[0-9A-Za-z-_]+)/page/(?P<page>\d+)/{0,1}$',
        views.tags_sub_tag,
        name='posts_tags_sub_tag'
    ),

    url(r'^(?P<slug>[0-9A-Za-z-_]+)/(?P<sub_slug>[0-9A-Za-z-_]+)/{0,1}$',
           views.tags_sub_tag,
           name='posts_tags_sub_tag'
    ),


    url(r'^videos/(?P<slug>[0-9A-Za-z-_]+)/(?P<sub_slug>[0-9A-Za-z-_]+)/page/(?P<page>\d+)/{0,1}$',
        views.video_tags_sub_tag,
        name='videos_tags_sub_tag'
    ),

    url(r'^videos/(?P<slug>[0-9A-Za-z-_]+)/(?P<sub_slug>[0-9A-Za-z-_]+)/{0,1}$',
           views.video_tags_sub_tag,
           name='videos_tags_sub_tag'
    ),


    url(r'^archive/(?P<year>[0-9A-Za-z-_]+)/(?P<month>[0-9A-Za-z-_]+)/page/(?P<page>\d+)/{0,1}$',
        views.year_month_archive,
        name='year_month_archive'
    ),

    url(r'^archive/(?P<year>[0-9A-Za-z-_]+)/(?P<month>[0-9A-Za-z-_]+)/{0,1}$',
           views.year_month_archive,
           name='year_month_archive'
    ),



    
]