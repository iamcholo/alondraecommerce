
from django.conf import settings
from django import template
from django.utils import timezone
from django.db.models import Q
from globaly.models import GlobalyTags
import mistune

register = template.Library()


@register.assignment_tag(name='get_tags', takes_context=True)
def get_tags(context):
    current_date =  timezone.now()
    f1 = Q(publish=True)
    tags = GlobalyTags.objects.filter(  f1 ).order_by('-id') 
    return tags
 
