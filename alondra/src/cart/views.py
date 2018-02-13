import urllib
from django.http import Http404
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from cart2 import Cart,Cart2, CART_ID, ItemAlreadyExists
from django.utils import timezone
from django.core.urlresolvers import reverse
from posts.models import PostItem
from django.shortcuts import get_object_or_404
from user_site.models import UserSite
from user_site.decorators import login_required
from django.conf import settings

def add_to_cart(request, product_id, variation=0 ):
    quantity = 1
   
    product = get_object_or_404(PostItem,id=product_id )
    price = 0.00
    cart = Cart(request)
    variation = int(variation)
    if variation == 1 :
       price = product.pricing       
    if variation == 2 :
       price = product.pricing_comercial
    if variation == 3 :
       price = product.pricing_developer
    
    try:
        cart.add(product, price, quantity)
    except ItemAlreadyExists: 
        cart.update(product, quantity, price)
    my_url = reverse("get_cart")
    return HttpResponseRedirect(my_url)

def remove_from_cart(request, product_id):
    product = PostItem.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    my_url = reverse("get_cart")
    return HttpResponseRedirect(my_url)

@login_required
def get_cart(request):
    context = {
        'vat':  0.00,
        'total': 0.00,
        'subtotal': 0.00,
        'count': 0,
        'cart': Cart(request),     
    }
    
    template_name = 'modules/cart/cart.html'
   
    context['count'] = dir(context['cart'])

    for c in context['cart'].items():
        context['total'] += c.product.pricing
   
    return TemplateResponse(request, template_name, context)

def clear_cart(request):    
    cart = Cart(request)
    cart.clear()
    my_url = reverse("get_cart")
    return HttpResponseRedirect(my_url)

