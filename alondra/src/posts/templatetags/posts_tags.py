
from django.conf import settings
from django import template
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
#from posts.models import PostCategory
from posts.models import PostItem
from utilities.paginator import paginator
from utilities.media import get_oembed
from utilities.media import add_img_class
import mistune

register = template.Library()

@register.assignment_tag(name='get_categories_nav')
def get_categories_nav():
    f1 = Q(publish=True)
    return PostCategory.objects.filter(f1)

@register.assignment_tag(name='get_features_articles', takes_context=True)
def get_features_articles(context, limit=5,post_type="post",exclude=None):
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)    
    f4 = Q(is_featured=True)   
    f5 = Q(post_type=post_type)     
    post = PostItem.objects.filter(  f1 & (f2 | f3)  & f4 & f5 ).order_by("-publish_date",'-id')[:limit]    
    return post
 

@register.assignment_tag(name='get_featured_article', takes_context=True)
def get_featured_article(context,post_type="post"):
    current_date =  timezone.now()
    limit = 1
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)    
    f4 = Q(is_featured=True)   
    f5 = Q(post_type=post_type)     
    post = PostItem.objects.filter(  f1 & (f2 | f3)  & f4 & f5 ).order_by("-publish_date",'-id')[:limit]    
    
    return next(iter(post),None)
   
@register.assignment_tag(name='get_featured_article_category', takes_context=True)
def get_featured_article_category(context,post_type="post",category_slug=None):
    current_date =  timezone.now()
    limit = 1
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)    
    f4 = Q(is_featured=True)
    f5 = Q(post_type=post_type)
    f6 = Q() 
    if category_slug is not None:
        f6 = Q(categories__slug=category_slug)
     
    post = PostItem.objects.filter(  f1 & (f2 | f3)  & f4 & f5 & f6 ).order_by("-publish_date",'-id')[:limit]    
    
    return next(iter(post),None)

@register.assignment_tag(name='get_recent_articles', takes_context=True)
def get_recent_articles(context, limit=10,post_type="post"):
    page = context.get('page',1)
    #lt for less than
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)     
    f4 = Q(post_type=post_type)      
    f5 = Q(is_on_feed=False)  
    return paginator(
            page, 
            PostItem.objects.filter(f1 & (f2 | f3) & f4 ).exclude(f5).order_by("-publish_date",'-id'),
            limit
        )

@register.assignment_tag(name='get_recent_articles_by_tags', takes_context=True)
def get_recent_articles_by_tags(context, limit=4,post_type="post",tags_slug=None):
    page = context.get('page',1)
    #lt for less than
    
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)     
    f4 = Q(post_type=post_type)      
    f5 = Q(is_on_feed=True)  
    f6 = Q(tags__slug=tags_slug) 
    post = paginator(
            page, 
            PostItem.objects.filter(f1 & (f2 | f3) & f4 & f5 & f6 ).order_by("-publish_date",'-id'),
            limit
        )
    return post

@register.assignment_tag(name='get_features_articles_by_tags', takes_context=True)
def get_features_articles_by_tags(context, limit=5,post_type="post",tags_slug=None):
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)    
    f4 = Q(is_featured=True)   
    f5 = Q(post_type=post_type)     
    f6 = Q(tags__slug=tags_slug) 

    post = PostItem.objects.filter(  f1 & (f2 | f3)  & f4 & f5 & f6 ).order_by("-publish_date",'-id')[:limit]    
    
    return post
 

@register.assignment_tag(name='get_recent_articles_category', takes_context=True)
def get_recent_articles_category(context, limit=10,post_type="post",category_slug=None):
    page = context.get('page',1)
    #lt for less than
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)     
    f4 = Q(post_type=post_type)      
    f5 = Q(is_on_feed=False)  
    f6 = Q() 
    if category_slug is not None:
        f6 = Q(categories__slug=category_slug)


    return paginator(
            page, 
            PostItem.objects.filter(f1 & (f2 | f3) & f4 & f6 ).exclude(f5).order_by("-publish_date",'-id'),
            limit
        )


@register.assignment_tag(name='count_articles_by_tag', takes_context=True)
def count_articles_by_tag(context, post_type="post",tags_slug=None):
    
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)     
    f4 = Q(post_type=post_type)      
    f5 = Q(is_on_feed=True)  
    f6 = Q(tags__slug=tags_slug) 
          
    posts = PostItem.objects.filter(f1 & (f2 | f3) & f4 & f5 & f6 ).annotate(total=Count('id')).order_by("-publish_date",'-id')
    
    return len(posts)


@register.assignment_tag(name='count_articles_by_year', takes_context=True)
def count_articles_by_year(context, post_type="post",tags_slug=None):
    
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)     
    f4 = Q(post_type=post_type)      
    f5 = Q(is_on_feed=True)  
    f6 = Q(tags__slug=tags_slug) 
           
    posts = PostItem.objects.filter(f1 & (f2 | f3) & f4 & f5 & f6 ).order_by("-publish_date",'-id')
            
    return len(posts)


@register.assignment_tag(name='count_articles_by_month', takes_context=True)
def count_articles_by_month(context, post_type="post",month="01"):
    
    current_date =  timezone.now()
    f1 = Q(publish=True)
    f2 = Q(publish_date__lte=current_date)
    f3 = Q(publish_date=None)     
    f4 = Q(post_type=post_type)      
    f5 = Q(is_on_feed=True)  
   
    f7 = Q(created__month=month)
           
    posts = PostItem.objects.filter(f1 & (f2 | f3) & f4 & f5 & f7 ).order_by("-publish_date",'-id')
    print posts     
    return len(posts)




@register.assignment_tag(name='get_articles_by_year', takes_context=True)
def get_articles_by_year(context):
    
 

    posts = PostItem.SitemapToYear()
   
    return posts




@register.assignment_tag(name='get_oembed_object', takes_context=True)
def get_oembed_object(context, item):
    request = context['request']
    BotNames=[
        'Googlebot',
        'Slurp',
        'Twiceler',
        'msnbot',
        'KaloogaBot',
        'YodaoBot',
        '"Baiduspider',
        'googlebot',
        'Speedy Spider',
        'DotBot'
    ]
    user_agent=request.META.get('HTTP_USER_AGENT',None)
    if not user_agent in BotNames:
        return  get_oembed(item)
    return  item

@register.filter
def get_markdown(item):
    renderer = mistune.Renderer(escape=False, hard_wrap=True)
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(item)

@register.filter
def add_img_class_boostrap(item):

    return add_img_class(item)


    