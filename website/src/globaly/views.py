from django.shortcuts import get_object_or_404
from utilities.paginator import paginator
from django.template.response import TemplateResponse
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db.models import Q
from itertools import chain
from django.utils import timezone
from django.shortcuts import render
from globaly.models import GlobalyTags
from globaly.models import GlobalyUrls

#from posts.models import PostItem
from django.shortcuts import render_to_response
from django.template import RequestContext

#DATE_FIELD_MAPPING = {
#    #VideoItem: 'created',
#    PostItem: 'created'
#}
#
#def my_key_func(obj):
#    return getattr(obj, DATE_FIELD_MAPPING[type(obj)])
#
#def tag(request, model, slug, page=1):
#    
#    template_name = 'modules/globaly/tags.html'
#    context = {}
#    context['tag'] = model
#    f1 = Q(tags__id=context['tag'].id)
#    qs = sorted(
#            #chain(
#                
#                PostItem.objects.filter( f1 ).order_by('-id'),
#            #),
#            key=my_key_func,
#            reverse=True
#        )  
#    context['posts'] = paginator(
#            page, 
#            qs
#            )
#    context['page'] = page
#   
#    return TemplateResponse(
#            request, 
#            template_name, 
#            context
#        )
#
#
#def search(request, page=1):
#    
#    template_name = 'modules/globaly/search.html' 
#    context = {}
#
#    if request.method == "POST":
#        x = request.POST
#        context['search_form'] = SearchForm(data=x)
#        
#        if context['search_form'].is_valid():
#            q = context['search_form'].cleaned_data['q']
#            if (len(q) > 0):                
#                request.session['search_q'] = q
#    
#    q = request.session.get('search_q', None)
#    
#    if not request.method == "POST":
#        context['search_form'] = SearchForm(
#            initial={
#                'q':q,
#            })
#
#    current_date =  timezone.now()
#    f1 = Q()
#    f2 = Q(publish_date__lte=current_date)
#    f3 = Q(publish_date=None)
#    f4 = Q(post_type="post") 
#    f5 = Q(post_type="page") 
#    f6 = Q(publish=True)
#    if q is not None:
#        f1 = Q(title__icontains=q)
#
#    qs = sorted(
#            chain( 
#                PostItem.objects.filter(  f1 & (f2 | f3) & (f4 | f5) & f6  ).order_by('-id'),
#            ),
#            key=my_key_func,
#            reverse=True
#        )  
#    context['posts'] = paginator(
#            page, 
#            qs
#        )
#    context['page'] = page
#
#    context['search_page'] = True
#  
#
#    return TemplateResponse(
#            request, 
#            template_name, 
#            context
#        )
#
def handler404(request):

    template_name = '404.html'
    context = {}

    return  TemplateResponse(request, template_name, context)

def handler500(request):

    template_name = '500.html'
    context = {}

    return  TemplateResponse(request, template_name, context)