from django import template
register = template.Library()
from navigation.models import NavigationItem

@register.assignment_tag(name='get_navigation_items')
def get_navigation_items(position):
    return NavigationItem.objects.filter(position__name=position)

