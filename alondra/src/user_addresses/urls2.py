
from django.conf.urls import url
from user_addresses import views 
# Create your views here.
urlpatterns = [
    
  

    url(r'^search/page/(?P<page>\d+)/{0,1}$',
            views.search,
            name='search'
        ),


    
]