from django import template
register = template.Library()
@register.filter
def is_none(value):
    return len(value) > 0