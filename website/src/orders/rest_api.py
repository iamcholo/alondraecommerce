import json
import os 
import sys
import hashlib
import time
from django.conf import settings
from rest_framework.views import APIView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets, generics
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FileUploadParser
from rest_framework import generics
from taxes.models import Orders,OrderShippingItem
from user_addresses.rest_api import AddresessSerializer
from user.rest_authentication import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from decimal import Decimal as D
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    billing_addresss_id = serializers.ReadOnlyField(source='billing_addresss.id')
    shipping_addresss_id = serializers.ReadOnlyField(source='shipping_addresss.id')    
    class Meta:
        model = Orders
        fields =    (
            'id',
            'status',
            'autor',
            'billing_addresss_id',
            'shipping_addresss_id',
            'total',
            'created', 
            'modified',
        )

class OrderShippingItemSerializer(serializers.HyperlinkedModelSerializer):
    order_id = serializers.ReadOnlyField(source='order.id')
    product_id = serializers.ReadOnlyField(source='product.id')
    class Meta:
        model = OrderShippingItem
        fields =    (
            'id',
            'order_id',
            'product',
            'value',
            'price',
            'status',
            'carrier',
            'tracking_number',
            'created', 
            'modified',
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def order_list(request):
        
    if request.method == 'GET':
        media = Orders.objects.all()
        serializer = OrdersSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)



@api_view(['DELETE','PUT','POST'])
@permission_classes((IsAuthenticated,))
def order(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            order = Orders.objects.get(
                pk=int(pk)
            )
        except Orders.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
    if request.method == 'DELETE':
        order.delete()
    if request.method == 'POST':
        serializer = OrdersSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
 
    if request.method == 'PUT':
        serializer = OrdersSerializer(
            order,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )
