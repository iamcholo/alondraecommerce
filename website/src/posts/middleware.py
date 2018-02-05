from django.core.urlresolvers import resolve
import importlib
from django.http import Http404
from posts.models import PostCategory
from posts.models import PostItem
from django.utils import timezone
from django.db.models import Q

class BlogUrlsMiddleware(object):
    

    def get_my_view (self, model):
        app_label =  model._meta.app_label
        name = 'src.%s.views' % app_label
        module = importlib.import_module(name)
                        
        return getattr(module, model.view_name)

    def process_view(self, request, view_func, view_args, view_kwargs):
       
        request.name = view_kwargs.get ('name', None)
        current_url = resolve(request.path_info)
        url_name = current_url.url_name
        current_date =  timezone.now()
        if  url_name == 'page_details': 
            if view_kwargs.has_key('slug'):
                f1 = Q(publish=True)
                f2 = Q(publish_date__lte=current_date)
                f3 = Q(publish_date=None) 
                f4 = Q(slug=view_kwargs.get('slug'))

                try:
                    model = PostCategory.objects.get( f1 & f4 )
                    view_kwargs['model'] = model
                    view_func = self.get_my_view(model)
                    return view_func(request, *view_args, **view_kwargs)

                except PostCategory.DoesNotExist:
                    try:
                        model = PostItem.objects.get( f1 & (f2 | f3) & f4)
                        view_kwargs['model'] = model
                        
                        view_func = self.get_my_view(model)
                        return view_func(request, *view_args, **view_kwargs)
                    except PostItem.DoesNotExist:
                        pass
                raise Http404