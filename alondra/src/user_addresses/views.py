import urllib
from django.http import Http404
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from cart2 import Cart,Cart2, CART_ID, ItemAlreadyExists
from django.utils import timezone
from django.core.urlresolvers import reverse
from store.models import StoreItem
from django.shortcuts import get_object_or_404
from store_orders.models import StoreOrder, StoreOrderItem
from user_site.models import UserSite
from user_site.decorators import login_required
from django.conf import settings
from user_addresses.models import Addresess
from django.utils.translation import ugettext_lazy as _

@login_required
def add_shipping_address(request):
    try:
        a = Addresess.objects.get(
            autor=request.user, 
            address_type="billing"
        )
        request.session['shipping_address'] = a.id
    except Addresess.DoesNotExist:
        request.session['ERROR_MESSAGE'] = _('ADDRESS_EMPTY_LABEL')


    my_url = reverse("get_cart")
    return HttpResponseRedirect(my_url)

@login_required
def add_billing_address(request):
    try:
        a = Addresess.objects.get(
            autor=request.user, 
            address_type="shipping"
        )
        request.session['billing_address'] = a.id
    except Addresess.DoesNotExist:
        request.session['ERROR_MESSAGE'] = _('ADDRESS_EMPTY_LABEL')
    

    my_url = reverse("add_shipping_address")
    return HttpResponseRedirect(my_url)

