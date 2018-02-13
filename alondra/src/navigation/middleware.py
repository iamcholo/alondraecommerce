from django.core.urlresolvers import resolve

import importlib
from django.http import Http404
from navigation.models import NavigationItem

class UrlsMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
       
        request.name = view_kwargs.get ('name', None)
        current_url = resolve(request.path_info)
        url_name = current_url.url_name
     
        if  url_name == 'home': 

            if view_kwargs.has_key('slug'):

                try:
                    item = NavigationItem.objects.get(slug=view_kwargs.get('slug'))
                    model =  item.content_object
                    model.slug = item.slug
                    model.meta_title = item.meta_title
                    model.meta_description = item.meta_description
                    if model is not None:
                        app_label =  model._meta.app_label
                        name = '%s.views' % app_label
                        module = importlib.import_module(name)
                        
                        view_kwargs['model'] = model
                        if view_kwargs.has_key('page'):
                            del view_kwargs['page']
                            #raise Http404()
                        view_func = getattr(module, model.view_name)
                        return view_func(request, *view_args, **view_kwargs)

                except NavigationItem.DoesNotExist:
                    
                    raise Http404()
