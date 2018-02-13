from posts.models import PostCategory
from posts.models import PostItem
from django.template.response import TemplateResponse
from django.utils import timezone
from itertools import chain
from django.db.models import Q

DATE_FIELD_MAPPING = {
    PostItem: 'created',
#   VideoItem: 'created',
}

def my_key_func(obj):
    return getattr(obj, DATE_FIELD_MAPPING[type(obj)])

def rss(request):    
    template_name = 'modules/rss/rss.xml' 
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f4 = Q(post_type="post")    


    context = {
        'posts':  sorted(
            #chain(
                #VideoItem.objects.filter(publish=True).order_by('-id'),
                PostItem.objects.filter( f1 & (f2 | f3) & f4  ).order_by('-id'),
            #),
            key=my_key_func,
            reverse=True
        )
    }

    return TemplateResponse(
            request, 
            template_name, 
            context, 
            content_type="text/xml"
        )
