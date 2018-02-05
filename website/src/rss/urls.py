from django.conf.urls import url
from utilities.generic.base import TemplateView
from rss import views 
# Create your views here.
urlpatterns = [
    url(r'^rss.xml$',
            views.rss,
            name='rss'
        ),   
]