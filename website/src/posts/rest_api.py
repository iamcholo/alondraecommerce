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
from posts.models import PostCategory
from posts.models import PostItem
from posts.models import Attributes,ProductAttributes
from globaly.models import GlobalyTags
from taxes.models import Taxes
from taxes.rest_api import TaxesSerializer
from globaly.rest_api import GlobalyTagsSerializer
from media.models import MediaAlbum,MediaImage
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
from navigation.models import NavigationItem


class AttributesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attributes
        fields =    (
            'id', 
            'archetype',
            'name',
            'priceable',
            'created', 
            'modified',
        )


class ProductAttributesSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    attributes_id = serializers.ReadOnlyField(source='attributes.id')
    class Meta:
        model = ProductAttributes
        fields =    (
            'id', 
            'product_id',
            'attributes_id',
            'value',
            'price',
            'created', 
            'modified',
        )

class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostCategory
        fields =    (
            'id', 
            'name',
            'slug',
            'meta_title',
            'meta_description',
            'publish',
            'post_type', 
            'created', 
            'modified',
        )

class PostItemSerializer(serializers.HyperlinkedModelSerializer):
    categories_lists = PostCategorySerializer(source='categories', many=True, read_only = True)
    tags_lists = GlobalyTagsSerializer(source='tags', many=True, read_only = True)
    taxes_lists = TaxesSerializer(source='taxes', many=True, read_only = True)
    autor_id = serializers.ReadOnlyField(source='autor.id')

    class Meta:
        model = PostItem
        fields = (
            'id',
            'autor_id',
            'categories_lists',
            'tags_lists',
            'taxes_lists',
            'title',
            'slug',
            'meta_title',
            'meta_description',
            'publish',
            'thumbnail',
            'thumbnail_text',
            'featured_image',
            'featured_image_text',
            'content',
            'excerpt',
            'publish_date',
            'featured_start_date',
            'featured_end_date',
            'post_type',
            'is_featured',
            'is_on_feed',
        )
 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_list(request):
        
    if request.method == 'POST':
        post_type = request.data.get('post_type','post')

        posts = PostItem.objects.filter(post_type=post_type).order_by('-id')
        serializer = PostItemSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_details(request):
    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            post = PostItem.objects.get(
                pk=pk
            )
        except PostItem.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostItemSerializer(
            post,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['PUT','POST','DELETE'])
@permission_classes((IsAuthenticated,))
def post(request):
    
    if request.method == 'POST':
        data= {}
        data.update({
            "title": "please write the project title",
            "slug": "please-write-the-project-title",
            "meta_title": "please write the project title",
            "meta_description": "",
            "content": "sample text",        
            "publish": False,
            'price': 0.00,
            'currency':'USD',
            'status':'pending',
        })
        serializer = PostItemSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(autor=request.user)

            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )      
    if request.method == 'PUT' or request.method == 'DELETE':
        try:
            pk = request.data.get('id')
            post = PostItem.objects.get(
                pk=int(pk)
            )
        except PostItem.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'PUT':
            serializer = PostItemSerializer(
                post,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                if request.data.has_key('categories_lists'):
                    d = request.data['categories_lists']
                    data = [ value.get('id') for value in d]
                    categories = PostCategory.objects.filter(                   
                        pk__in=data
                    )
                    serializer.save(
                        categories=categories                      
                    )

               
                if request.data.has_key('tag_lists'):
                 
                    t = request.data['tag_lists']
                    data = [ value.get('id') for value in t]
                    tags = GlobalyTags.objects.filter(                   
                        pk__in=data
                    )
                    serializer.save(
                       tags=tags                     
                    )

                           
                if request.data.has_key('taxes_lists'):
                 
                    t = request.data['taxes_lists']
                    data = [ value.get('id') for value in t]
                    taxes = Taxes.objects.filter(                   
                        pk__in=data
                    )
                    serializer.save(
                       taxes=taxes                     
                    )

                  
                    
                instance = serializer.instance
                try:
                    f1 = Q(app_label='posts')
                    f2 = Q(model='PostItem')
                    i = ContentType.objects.get(
                        f1 & f2
                        )
                    #i.get_object_for_this_type(id=pk)
                    cType = ContentType.objects.get_for_model( 
                        i.get_object_for_this_type(id=pk)
                    )
                    #custom view codes here in the future implement signal
                    post_type = request.data.get('post_type','post')
                    view_name = "post_details"
                    
                    if(post_type=="page"):
                        view_name = "page_details"
                    
                    if(post_type=="game"):
                        view_name = "game_details"

                    parent = NavigationItem.objects.filter(
                        object_id=pk,
                        content_type=cType,
                        view_name=view_name
                    ).update(slug=request.data.get('slug'))                   
                except ObjectDoesNotExist:
                    return None
                return Response(serializer.data)

        if request.method == 'DELETE':
            post.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def categories_list(request):

    if request.method == 'GET':
        posts = PostCategory.objects.all().order_by('-id')
        serializer = PostCategorySerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def category_details(request):
    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            category = PostCategory.objects.get(
                pk=pk
            )
        except PostCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostCategorySerializer(
            category,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )


@api_view(['PUT','POST','DELETE'])
@permission_classes((IsAuthenticated,))
def category(request):
    
    if request.method == 'POST':
        serializer = PostCategorySerializer(
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
            category = PostCategory.objects.get(
                pk=int(pk)
            )
        except PostCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'PUT':
            serializer = PostCategorySerializer(
                category,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                instance = serializer.instance
                try:
                    f1 = Q(app_label='posts')
                    f2 = Q(model='PostCategory')
                    i = ContentType.objects.get(
                        f1 & f2
                        )
                         
                    cType = ContentType.objects.get_for_model(
                        i.get_object_for_this_type(id=pk)
                    )
                    parent = NavigationItem.objects.filter(
                        object_id=pk,
                        content_type=cType,
                        view_name='category'
                    ).update(slug=request.data.get('slug')) 
                                   
                except ObjectDoesNotExist:
                    return None
                return Response(serializer.data)

        if request.method == 'DELETE':
            category.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    





@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def attributes_list(request):

    if request.method == 'GET':
        posts = Attributes.objects.all().order_by('-id')
        serializer = AttributesSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def attribute_details(request):
    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            attribute = Attributes.objects.get(
                pk=pk
            )
        except Attributes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AttributesSerializer(
            attribute,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )


@api_view(['PUT','POST','DELETE'])
@permission_classes((IsAuthenticated,))
def attribute(request):
    
    if request.method == 'POST':
        serializer = AttributesSerializer(
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
            attribute = Attributes.objects.get(
                pk=int(pk)
            )
        except Attributes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'PUT':
            serializer = AttributesSerializer(
                attribute,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data)

        if request.method == 'DELETE':
            attribute.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    
