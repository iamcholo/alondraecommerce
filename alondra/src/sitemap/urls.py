from django.conf.urls import url
from utilities.generic.base import TemplateView
from sitemap import views 
# Create your views here.
urlpatterns = [

    url(r'^sitemap_index\.xml$',
            views.home,
            name='sitemap_home'
        ),

    url(r'^sitemap-misc\.xml$',
            views.misc,
            name='sitemap_misc'
        ),

    url(r'^xml-sitemap\.xsl$',
        TemplateView.as_view(
            template_name='modules/sitemap/xml-sitemap.xsl', 
            content_type='text/xml'
        ), 
        name='sitemap_xsl_theme'
    ), 

    url(r'^xml-sitemap-dated\.xsl$',
        TemplateView.as_view(
            template_name='modules/sitemap/xml-sitemap-dated.xsl', 
            content_type='text/xml'
        ), 
        name='sitemap_xsl_theme_dated'
    ),  

    url(r'^xml-sitemap_normal\.xsl$',
        TemplateView.as_view(
            template_name='modules/sitemap/xml-sitemap_normal.xsl', 
            content_type='text/xml'
        ), 
        name='sitemap_xsl_theme_normal'
    ),  
    url(r'^post-items-pt-(?P<slug>[0-9A-Za-z-_]+)\.xml/{0,1}$',
        views.details,
        name='sitemap_details'),

]