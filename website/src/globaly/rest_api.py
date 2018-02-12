import json
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets, generics
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from globaly.models import GlobalyTags
from django.contrib.auth.models import User
from user.rest_authentication import IsAuthenticated
from django.db.models import Q
from decimal import Decimal as D
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


class GlobalyTagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlobalyTags
        fields =    (
            'id', 
            'name',
            'slug',
            'meta_title',
            'meta_description',
            'publish',
            'created', 
            'modified',
        )

@api_view(['GET'])
def tag_list(request):

    if request.method == 'GET':
        tags = GlobalyTags.objects.all()
        serializer = GlobalyTagsSerializer(
            tags, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST'])
def tag_details(request):
    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            tag = GlobalyTags.objects.get(
                pk=pk
            )
        except GlobalyTags.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = GlobalyTagsSerializer(
            tag,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )


@api_view(['PUT','POST','DELETE'])
def tag(request):
    
    if request.method == 'POST':
        serializer = GlobalyTagsSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )      
    if request.method == 'PUT' or request.method == 'DELETE':
        try:
            pk = request.data.get('id')
            tag = GlobalyTags.objects.get(
                pk=int(pk)
            )
        except GlobalyTags.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'PUT':
            serializer = GlobalyTagsSerializer(
                tag,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                instance = serializer.instance
                try:
                    f1 = Q(app_label='globaly')
                    f2 = Q(model='GlobalyTags')
                    i = ContentType.objects.get(
                        f1 & f2
                        )
                         
                    cType = ContentType.objects.get_for_model(
                        i.get_object_for_this_type(id=pk)
                    )
                    parent = NavigationItem.objects.filter(
                        object_id=pk,
                        content_type=cType,
                        view_name='tags'
                    ).update(slug=request.data.get('slug')) 
                                   
                except ObjectDoesNotExist:
                    return None
                return Response(serializer.data)

        if request.method == 'DELETE':
            tag.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    
