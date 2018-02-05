import re
from django.conf import settings
from django import template
from django.utils import timezone
from bs4 import BeautifulSoup, Tag
from django.db.models import Q
from media.models import MediaImage

register = template.Library()
regex = re.compile(r'\[album\](.*?)\[\/album\]+')
regex2 = re.compile(r'\<p\>(\[album\].*\[\/album\])\<\/p\>+')
"""
ussage |get_markdown|album_short_code
this need to be improved
"""
@register.filter
def album_short_code(content, replace_parent=False):
   
    for item in regex2.findall(unicode(content)):
        g = re.search(regex,item) 
        pk = g.group(1)
        image = ""
        images = MediaImage.objects.filter(album__id=pk).order_by('id')
        
        if len(images)>0:
            
            for img in images:
                image += "<div><img src='{0}' title='{1}' alt='{1}' /></div>".format(img.image.url, img.title)
            
            new_div = "<div class='gallery' data-id='%s'>%s</div>" % (pk, image) 
            regex3 = re.compile('\<p\>(\[album\]%s\[\/album\])\<\/p\>+'% pk)
            content = re.sub(regex3, new_div, unicode(content))

    return content

@register.assignment_tag(name='get_features_images_by_tags', takes_context=True)
def get_features_images_by_tags(context, limit=5,tags_slug=None):
    current_date =  timezone.now()
    f6 = Q(tags__slug=tags_slug) 
    post = MediaImage.objects.filter(   f6 ).order_by('-id')[:limit]    
    return post
 
@register.assignment_tag(name='get_media_image', takes_context=True)
def get_media_image(context, slug=None):
    f6 = Q(title=slug) 
    image = MediaImage.objects.filter(f6).order_by('-id')
    return next(iter(image),None)
      