from django.conf.urls import  include, url
from django.conf import settings
from django.conf.urls.static import static
from utilities.generic.base import TemplateView
from utilities.rest_api_urls import router, apiurls
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = [

    url(r'^api/', include(apiurls)),
    url(r'^admin/$',
        TemplateView.as_view(
            template_name='index.html', 
            content_type='text/html'
        ), 
        name='admin'
    ),
    url(r'^archivos/$',
        TemplateView.as_view(
            template_name='archive.html', 
            content_type='text/html'
        ), 
        name='archive'
    ),
    url(r'', include('posts.urls2')),
    url(r'^', include("sitemap.urls")),
    url(r'^', include("rss.urls")),
    #url(r'^mediaframework/', include("media.urls")),
    url(r'^comments/', include("comments.urls2")),
    #url(r'^admin/kawai/', include(admin.site.urls)),
  

    url(r'^robots\.txt$', 
        TemplateView.as_view(
            template_name='robots.txt', 
            content_type= 'text/plain'
        ),
        name='robots'
    ),

    url(r'^(?P<page>\d+)/{0,1}$',
        TemplateView.as_view(
            template_name='home.html', 
            content_type='text/html'
        ), 
        name='home'
    ), 
    url(r'^$',
        TemplateView.as_view(
            template_name='home.html', 
            content_type='text/html'
        ), 
        name='home'
    ),
    url(r'^(?P<slug>[-\w\d]+)/(?P<page>\d+)/{0,1}$',
        TemplateView.as_view(
         template_name='home.html', 
         content_type='text/html'
        ), 
        name='page_details'
    ),

    url(r'^(?P<slug>[-\w\d]+)/{0,1}$',
        TemplateView.as_view(
         template_name='home.html', 
         content_type='text/html'
        ), 
        name='page_details'
    ),

  


 

] 


urlpatterns += static(
    settings.STATIC_URL, 
    document_root=settings.STATIC_ROOT
) 


urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_UPLOAD_ROOT
)


handler404 = "globaly.views.handler404"
handler500 = "globaly.views.handler500"
