from django import template
register = template.Library()


@register.filter(name='has_attr')
def has_attr(item, attr):
    return hasattr(item,attr)