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
from taxes.models import Taxes
from user.rest_authentication import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from decimal import Decimal as D
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class TaxesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxes
        fields =    (
            'id',
            'city',
            'country',
            'percent',
            'created', 
            'modified',
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def taxes_list(request):
        
    if request.method == 'POST':
        media = Taxes.objects.all()
        serializer = TaxesSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def taxes_create(request):
        
    if request.method == 'POST':
        serializer = TaxesSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(
                    product=product
                )
           
            return Response(serializer.data)     
            
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def taxes_details(request):
    
    try:
        pk = request.data.get('id')
        tax = Taxes.objects.get(
            pk=int(pk)
        )
    except Taxes.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'POST':
        serializer = TaxesSerializer(
            tax,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )



@api_view(['DELETE','PUT','POST'])
@permission_classes((IsAuthenticated,))
def tax(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            tax = Taxes.objects.get(
                pk=int(pk)
            )
        except Taxes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
    if request.method == 'DELETE':
        tax.delete()
    if request.method == 'POST':
        serializer = TaxesSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
 
    if request.method == 'PUT':
        serializer = TaxesSerializer(
            tax,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )
