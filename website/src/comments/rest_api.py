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
from comments.models import Comments
from django.contrib.auth.models import User
from user.rest_authentication import IsAuthenticated
from django.db.models import Q
from decimal import Decimal as D
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comments
        fields =    (
            'id', 
            'comment',
            'email',
            'name',
            'website',
            'status',           
            'created', 
            'modified',
        )

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def comments(request):
        
    if request.method == 'GET':
        comments = Comments.objects.all()
        serializer = CommentsSerializer(
            comments, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['PUT','POST','DELETE'])
@permission_classes((IsAuthenticated,))
def comment(request):
    
    if request.method == 'POST':
        serializer = CommentsSerializer(
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
            comment = Comments.objects.get(
                pk=int(pk)
            )
        except Comments.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'PUT':
            serializer = CommentsSerializer(
                comment,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        if request.method == 'DELETE':
            comment.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    
