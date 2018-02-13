from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone
from utilities.paginator import paginator
from posts.models import PostCategory
from posts.models import PostItem
from globaly.models import GlobalyTags
from posts.forms import SearchForm
from django.shortcuts import get_object_or_404

def category(request, slug=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f6 = Q(slug=slug)

    if model is None:
        model = get_object_or_404(PostCategory, f1 & f6 )
    
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f4 = Q(categories__id=model.id)    
    f5 = Q(post_type="post")    

    context['category'] = model
    context['slug'] = slug    
    context['page'] = int(page)    
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3) & f4 & f5
                ).order_by("-publish_date",'-id')
                
            )
   

    template_name = [
            'modules/%s/category-%d.html' % (model.post_type, model.id),
            'modules/%s/category-%s.html' % (model.post_type, slug),
            'modules/%s/category.html' % model.post_type
        ]
    return TemplateResponse(request, template_name, context)

def post_details(request, slug=None, model=None):
    
    context = {}
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None) 
    f4 = Q(slug=slug)
    f5 = Q(post_type='post') 

    if model is None:
        model = get_object_or_404(PostItem, f1 & (f2 | f3) & f4 & f5 )
    
    context['post'] = model
    context['related_posts'] = context['post'].related_posts.filter( 
            f1 & (f2 | f3) 
        ).order_by("-publish_date",'-id')

    context['tags'] = context['post'].tags.all()
    
    template_name =  [
            'modules/%s/post-%d.html' % (model.post_type, model.id),
            'modules/%s/post-%s.html' % (model.post_type, slug),
            'modules/%s/post.html' % model.post_type,
            
        ] 
    return TemplateResponse(request, template_name, context)

def page_details(request, slug=None, model=None):
    
    context = {}
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None) 
    f4 = Q(slug=slug)
    f5 = Q(post_type='page') 

    if model is None:
        model = get_object_or_404(PostItem, f1 & (f2 | f3) & f4 & f5  )
    
    context['post'] = model
    context['related_posts'] = context['post'].related_posts.filter( 
            f1 & (f2 | f3) 
        ).order_by("-publish_date",'-id')

    context['tags'] = context['post'].tags.all()
    
    template_name =  [
            'modules/%s/post-%d.html' % (model.post_type, model.id),
            'modules/%s/post-%s.html' % (model.post_type, slug),
            'modules/%s/post.html' % model.post_type,
            
        ] 
    return TemplateResponse(request, template_name, context)


def video_details(request, slug=None, model=None):
    
    context = {}
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None) 
    f4 = Q(slug=slug)
    f5 = Q(post_type='page') 

    if model is None:
        model = get_object_or_404(PostItem, f1 & (f2 | f3) & f4 & f5  )
    
    context['post'] = model
    context['related_posts'] = context['post'].related_posts.filter( 
            f1 & (f2 | f3) 
        ).order_by("-publish_date",'-id')

    context['tags'] = context['post'].tags.all()
    
    template_name =  [
            'modules/%s/post-%d.html' % (model.post_type, model.id),
            'modules/%s/post-%s.html' % (model.post_type, slug),
            'modules/%s/post.html' % model.post_type,
            
        ] 
    return TemplateResponse(request, template_name, context)



def autor(request, slug=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f4 = Q(autor__nick=slug)    
    f5 = Q(post_type="post")

    post_type = "post"
    context['slug'] = slug
    context['autor'] = slug

    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3) & f4 & f5 
                ).order_by("-publish_date",'-id')
                
            )

    template_name = [
            #'modules/%s/autor-%d.html' % (post_type, model.id),
            'modules/%s/autor-%s.html' % (post_type, context['autor']),
            'modules/%s/autor.html' % post_type
        ]
    return TemplateResponse(request, template_name, context)

def tags(request, slug=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f4 = Q(tags__slug=slug)    
    f5 = Q(post_type="post")  

    post_type = "post"
    context['slug'] = slug
    context['tag'] = get_object_or_404( GlobalyTags,slug=slug)
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3) & f4 & f5 
                ).order_by("-publish_date",'-id')
                
            )

    template_name = [
            #'modules/%s/autor-%d.html' % (post_type, model.id),
            'modules/%s/tag-%s.html' % (post_type, context['tag']),
            'modules/%s/tag.html' % post_type
        ]
    return TemplateResponse(request, template_name, context)


def tags_sub_tag(request, slug=None,sub_slug=None,  page=1):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f5 = Q(categories__slug=sub_slug)
    f4 = Q(tags__slug__in=[slug])
    

    context['slug'] = slug
    context['sub_slug'] = sub_slug
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3) & f4 & f5 
                ).order_by("-publish_date",'-id')
                
            )
    post_type = 'post'
    template_name = [
            #'modules/%s/autor-%d.html' % (post_type, model.id),
            'modules/%s/tag.html' % post_type
        ]
    return TemplateResponse(request, template_name, context)


def video_tags_sub_tag(request, slug=None,sub_slug=None,  page=1):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f5 = Q(categories__slug=sub_slug)
    f4 = Q(tags__slug__in=[slug])
    f6 = Q(post_type="video")  

    context['slug'] = slug
    context['sub_slug'] = sub_slug
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3) & f4 & f5 & f6
                ).order_by("-publish_date",'-id')
                
            )
    post_type = 'video'
    template_name = [
            #'modules/%s/autor-%d.html' % (post_type, model.id),
            'modules/%s/tag.html' % post_type
        ]
    return TemplateResponse(request, template_name, context)


def games(request, slug=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f5 = Q(post_type="game")  
    
    context['slug'] = slug
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3)  & f5
                ).order_by("-publish_date",'-id')
                
            )
   

    template_name = [            
            'modules/%s/category.html' % 'game'
        ]
    return TemplateResponse(request, template_name, context)


def videos(request, slug=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f5 = Q(post_type="video")  
    
    context['slug'] = slug
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3)  & f5
                ).order_by("-publish_date",'-id')
                
            )
   

    template_name = [            
            'modules/%s/category.html' % 'video'
        ]
    return TemplateResponse(request, template_name, context)


def games_engines(request, slug=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f5 = Q(post_type="game_engine")  
    
    context['slug'] = slug
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3)  & f5
                ).order_by("-publish_date",'-id')
                
            )
   

    template_name = [            
            'modules/%s/category.html' % 'game_engine'
        ]
    return TemplateResponse(request, template_name, context)


def year_month_archive(request, year=None, month=None, page=1, model=None):

    context = {}
    current_date =  timezone.now()

    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)
    f5 = Q(post_type="post")  
    f6 = Q(created__year=year)  
    f7 = Q(created__month=month)  
    context['year'] = year
    context['month'] = month
    context['posts'] = paginator(
                page, 
                PostItem.objects.filter(
                    f1 & (f2 | f3)  & f5 & f6 & f7
                ).order_by("-publish_date",'-id')
                
            )
   

    template_name = [            
            'archive-year-month.html' 
        ]
    return TemplateResponse(request, template_name, context)




def search(request):

    context = {}
    current_date =  timezone.now()
    context['q'] = request.GET.get("q", None)
    context['page'] = request.GET.get("page", 1)
    if(len(context['q'])>0):
        f1 = Q(publish=True)
        f2 = Q(publish_date__lte=current_date)
        f3 = Q(publish_date=None)
        f5 = Q(post_type="page")  
        f6 = Q(title__icontains=context['q'])
        f7 = Q(post_type="post") 
        f8 = Q(post_type="game") 
        f9 = Q(post_type="game_engine") 
        f10 = Q(post_type="video") 

        context['posts'] = paginator(
                    context['page'], 
                    PostItem.objects.filter(
                        f1 & (f2 | f3)   & f6 & f7 
                    ).exclude(f5).order_by("-publish_date",'-id')
                    
                )
    else:
        context['posts'] = []

    template_name = [            
            'modules/%s/search.html' % 'search'
        ]
    return TemplateResponse(request, template_name, context)
