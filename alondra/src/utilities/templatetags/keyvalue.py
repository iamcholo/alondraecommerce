from django import template
from django.template import RequestContext
from django.template import Library, loader, Context

register = template.Library()
 
from django.template import Variable, VariableDoesNotExist
@register.filter
def keyvalue(object, attr):
    pseudo_context = { 'object' : object }
    try:
        value = Variable('object.%s' % attr).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
    return value