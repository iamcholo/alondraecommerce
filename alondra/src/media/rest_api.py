import json
import os 
import sys
import hashlib
import time
from django.conf import settings
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from media.models import MediaAlbum
from media.models import MediaImage
from globaly.models import GlobalyTags
from globaly.rest_api import GlobalyTagsSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



class MediaAlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MediaAlbum
        fields =    ('id','title','publish', 'created', 'modified',)


class MediaImage2Serializer(serializers.HyperlinkedModelSerializer):
    albums_lists = MediaAlbumSerializer(source='album', many=True, read_only = True)

    #image = Base64ImageField(
    #    max_length=None, use_url=True,
    #)    
    tags_lists = GlobalyTagsSerializer(source='tags', many=True, read_only = True)
    class Meta:
        model = MediaImage
        fields = (
            'id',
            'tags_lists',
            'albums_lists',
            'title',
            'image',  
            'created',
            'modified',

        )

class MediaImageSerializer(serializers.HyperlinkedModelSerializer):
    albums_lists = MediaAlbumSerializer(source='album', many=True, read_only = True)
    #image = Base64ImageField(
    #    max_length=None, use_url=True,
    #)    
    tags_lists = GlobalyTagsSerializer(source='tags', many=True, read_only = True)
    class Meta:
        model = MediaImage
        fields = (
            'id',
            'tags_lists',
            'title',
            'image',               
            'content',
            'created',
            'modified',
            'albums_lists'

        )

    def get_featured_imagex(self, ob):
        
        ids = [int(x.id) for x in ob.album.select_related() ] 
        i = MediaImage.objects.filter(album__id__in=ids).order_by('id')
        logo = settings.STATIC_URL + "img/avatar-250-250.gif" 
        if len(i) > 0:
            t = next(iter(i), logo)

            return t.get_logo()
        else: 
            return logo

@api_view(['GET'])
def media_list(request):
        
    if request.method == 'GET':
        media = MediaImage.objects.all()
        serializer = MediaImageSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['PUT'])
def image_create(request):
        
    if request.method == 'PUT':
        file_name = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        filenamex, file_extension = os.path.splitext(file_name.name)
        millis = int(round(time.time() * 1000))

        m = hashlib.sha224("%s%d" %(filenamex,millis)).hexdigest()
        filename = "%s%s" %(m,file_extension)
        url = 'uploads/%s'% filename
        file_path = os.path.join(file_path, filename)
        path = default_storage.save(
            file_path, 
            ContentFile(file_name.read())
        )
 
        image = MediaImage()
        image.title = request.data.get('name',None) or filenamex   
        image.image = url
        image.content = filenamex
        image.save()
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['POST'])
def image_details(request):
    
    try:
        pk = request.data.get('id')
        image = MediaImage.objects.get(
            pk=int(pk)
        )
    except MediaImage.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )


    if request.method == 'POST':
        serializer = MediaImage2Serializer(
            image,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )



@api_view(['DELETE','PUT','POST'])
def image(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            image = MediaImage.objects.get(
                pk=int(pk)
            )
        except MediaImage.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        if request.method == 'DELETE':
            image.delete()


    if request.method == 'POST':
        serializer = MediaImage2Serializer(
           
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            if request.data.has_key('tag_lists') \
            and not  request.data.has_key('album_lists'):
                t = request.data['tag_lists']
                data = [ value.get('id') for value in t]
                tags = GlobalyTags.objects.filter(                   
                    pk__in=data
                )
                serializer.save(
                   tags=tags                     
                )
            
               
            if request.data.has_key('album_lists') \
            and not  request.data.has_key('tag_lists') :
                t = request.data['album_lists']
                data = [ value.get('id') for value in t]
                album = MediaAlbum.objects.filter(                   
                    pk__in=data
                )
                serializer.save(
                   album=album                     
                )    

            if request.data.has_key('tag_lists') \
            and request.data.has_key('album_lists'):
                t = request.data['tag_lists']
                data = [ value.get('id') for value in t]
                tags = GlobalyTags.objects.filter(                   
                    pk__in=data
                )

                t = request.data['album_lists']
                data = [ value.get('id') for value in t]
                album = MediaAlbum.objects.filter(                   
                    pk__in=data
                )
                serializer.save(
                   tags=tags,
                   album=album                   
                )          
                 
            if not request.data.has_key('album_lists') \
                and not request.data.has_key('tag_lists'):
                 serializer.save()

            return Response(serializer.data)
           
    if request.method == 'PUT':
        serializer = MediaImage2Serializer(
            image,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            if request.data.has_key('tag_lists') \
            and not  request.data.has_key('album_lists'):
                t = request.data['tag_lists']
                data = [ value.get('id') for value in t]
                tags = GlobalyTags.objects.filter(                   
                    pk__in=data
                )
                serializer.save(
                   tags=tags                     
                )
            
               
            if request.data.has_key('album_lists') \
            and not  request.data.has_key('tag_lists') :
                t = request.data['album_lists']
                data = [ value.get('id') for value in t]
                album = MediaAlbum.objects.filter(                   
                    pk__in=data
                )
                serializer.save(
                   album=album                     
                )    

            if request.data.has_key('tag_lists') \
            and request.data.has_key('album_lists'):
                t = request.data['tag_lists']
                data = [ value.get('id') for value in t]
                tags = GlobalyTags.objects.filter(                   
                    pk__in=data
                )

                t = request.data['album_lists']
                data = [ value.get('id') for value in t]
                album = MediaAlbum.objects.filter(                   
                    pk__in=data
                )
                serializer.save(
                   tags=tags,
                   album=album                   
                )          
                 
            if not request.data.has_key('album_lists') \
                and not request.data.has_key('tag_lists'):
                 serializer.save()

            return Response(serializer.data)
        print serializer.errors
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )



@api_view(['GET'])
def media_album_list(request):
        
    if request.method == 'GET':
        media = MediaAlbum.objects.all()
        serializer = MediaAlbumSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
def media_album_create(request):
    
    if request.method == 'POST':
        serializer = MediaAlbumSerializer(
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
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['DELETE','PUT','POST'])
def media_album(request):
    try:
        pk = request.data.get('id')
        album = MediaAlbum.objects.get(
            pk=int(pk)
        )
    except MediaAlbum.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )   

    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            post = MediaAlbum.objects.get(
                pk=pk
            )
        except MediaAlbum.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MediaAlbumSerializer(
            post,
            context={'request': request}
        )
        return Response(serializer.data)

    if request.method == 'DELETE':
        album.delete()

    if request.method == 'PUT':

        serializer = MediaAlbumSerializer(
            album,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
           
            serializer.save()
         
            return Response(serializer.data)
        print serializer.errors
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )