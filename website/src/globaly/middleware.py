from django.core.urlresolvers import resolve
import importlib
from django.http import Http404
from globaly.models import GlobalyUrls

class SearchMiddleware(object):
    

    def process_view(self, request, view_func, view_args, view_kwargs):
       
        #request.name = view_kwargs.get ('name', None)
        current_url = resolve(request.path_info)
        url_name = current_url.url_name

        if  url_name is not 'search' and request.session.has_key('search_q'): 
            del request.session['search_q']
            request.session.modified = True

