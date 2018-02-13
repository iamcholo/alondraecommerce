
from django.conf import settings
from django import template
from django.utils import timezone
from comments.models import Comments
from comments.forms import CommentsModelForm
from django.db.models import Q
register = template.Library()

@register.inclusion_tag(  'modules/comments/includes/_comment_form.html' , takes_context=True)
def get_commment_form(context):
    return {
            "comment_form": CommentsModelForm(),
            'post': context['post']
        }

@register.inclusion_tag(  'modules/comments/includes/_recent_comments.html', takes_context=True)
def get_recent_comments(context, limit):
    f1 = Q(status='published')
    return Comments.objects.filter(  f1 )[:limit].order_by('-id')

@register.inclusion_tag('modules/comments/includes/_comments.html', takes_context=True)
def comments_pagination(context, target, page=1, limit=15):
    f1 = Q(status='published')
    f2 = Q(target__id=target)
    return paginator(
            page,
            Comments.objects.filter(f1 & f2),
            limit
        )

@register.assignment_tag(takes_context=True)
def list_comments(context, target_id, page=1, limit=15):
    f1 = Q(status='published')
    f2 = Q(target__id=target_id)
    return Comments.objects.filter(f1 & f2).order_by('id')
        

@register.filter()
def count_comment(target_id):
    f1 = Q(status='published')
    f2 = Q(target__id=target_id)
    return Comments.objects.filter(f1 & f2).count()
        

     