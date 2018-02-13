import json
import mercadopago
from django.conf import settings
from django.conf.urls import url, include
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils.translation import ugettext_lazy as _
from cart2 import Cart, CART_ID, ItemAlreadyExists
from posts.models import PostItem

@api_view(['POST'])
@permission_classes((AllowAny,))
def add_to_cart(request):

    data = {'success': False}
    if request.method == 'POST':
        product_id = request.data.get('pk')
        variation = request.data.get('variation')
        try:
            quantity=1
            product = PostItem.objects.get(id=product_id)
            price = 0.00
            if variation == 1 :
               price = product.pricing
            if variation == 2 :
               price = product.pricing_comercial
            if variation == 3 :
               price = product.pricing_developer
            try:
                cart = Cart(request)
                cart.add(product, price, quantity)
                data['success'] = True
            except ItemAlreadyExists: 
                pass
        except PostItem.DoesNotExist:
            pass

    return Response(
            data,
            status=status.HTTP_201_CREATED
        )
@api_view(['GET'])
@permission_classes((AllowAny,))
def count_cart_elements(request):
    cart =  Cart(request)
    data = {'Length': len(cart.items())}
    return Response(
            data,
            status=status.HTTP_201_CREATED
        )
