from django import template
register = template.Library()


@register.filter(name='key')
def key(dictionary, key):
    return dictionary.get(key)
