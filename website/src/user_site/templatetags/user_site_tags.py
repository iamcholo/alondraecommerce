from django import template
from utilities.image_base64 import encode_image
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
register = template.Library()
@register.assignment_tag(name='getencode_64')
def getencode_64(value,width=100,height=100):
    if value is not None:
        image = value.logo.name
        if len(image):
            return encode_image( image, value.id, width, height)
    return False

@register.filter(takes_context=True)
def form_error_list(k,form):       
	return str(form.fields[k].label)

@register.filter()
def is_valid_email( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False