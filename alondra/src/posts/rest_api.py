
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from navigation.models import NavigationItem
from posts.models import PostCategory
from posts.models import PostItem
from posts.models import Attributes,ProductAttributes
from media.rest_api import MediaAlbumSerializer
from globaly.models import GlobalyTags
from taxes.models import Taxes
from taxes.rest_api import TaxesSerializer
from globaly.rest_api import GlobalyTagsSerializer
from media.models import MediaAlbum,MediaImage


class ProductAttributesSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    attributes_id = serializers.ReadOnlyField(source='attributes.id')
    class Meta:
        model = ProductAttributes
        fields =    (
            'id', 
            'thumbnail',
            'thumbnail_text',
            'featured_image',
            'featured_image_text',
            'product_id',
            'attributes_id',
            'value',
            'price',
            'created', 
            'modified',
        )

class AttributesSerializer(serializers.HyperlinkedModelSerializer):
    child = serializers.SerializerMethodField('get_popularity')
    class Meta:
        model = Attributes
        fields =    (
            'id', 
            'archetype',
            'name',
            'child',
            'priceable',
            'created', 
            'modified',
        )
        

    def get_popularity(self, obj):

        request = self.context.get("request")
        if not request.data.has_key('product_id'):
            return None
        pk = request.data.get('product_id')
        pk2 = obj.id
        
       

        if obj.archetype in ['choices','selectable']:
            posts = ProductAttributes.objects.filter(
                    attributes__pk=pk2,
                    product__id=pk,
                ).order_by('-id')
            serializer = ProductAttributesSerializer(
                posts, 
                many=True,
                context={'request': request}
            )
            return serializer.data

        if obj.archetype in ['text','date']:
            try:


                attribute = ProductAttributes.objects.get(
                    attributes__pk=pk2,
                    product__id=pk,
                )
                serializer = ProductAttributesSerializer(
                    attribute,
                    context={'request': request}
                )
                return serializer.data

            except ProductAttributes.DoesNotExist:
                return None
        return None     
            


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
    album_lists = MediaAlbumSerializer(source='album', many=True, read_only = True)
    autor_id = serializers.ReadOnlyField(source='autor.id')

    class Meta:
        model = PostItem
        fields = (
            'id',
            'autor_id',
            'categories_lists',
            'tags_lists',
            'taxes_lists',
            'album_lists',
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

                if request.data.has_key('album_lists'):
                 
                    t = request.data['album_lists']
                    data = [ value.get('id') for value in t]
                    album = MediaAlbum.objects.filter(                   
                        pk__in=data
                    )
                    serializer.save(
                       album=album                     
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





@api_view(['GET','POST'])
def attributes_list(request):

    if request.method in ['GET','POST']:
        posts = Attributes.objects.all().order_by('-id')
        serializer = AttributesSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST'])
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

                if attribute.attribute != serializer.instance.archetype:

                    if serializer.instance.archetype in ['choices','selectable']:
                            
                        attributes = ProductAttributes.objects.filter(
                                attributes__pk=attribute.id,
                                
                            ).order_by('-id')
                        attributes.delete()
                        
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


@api_view(['GET'])
def attribute_products_list(request):

    if request.method == 'GET':
        pk = request.data.get('product_id')
        pk2 = request.data.get('attributes_id')
        posts = ProductAttributes.objects.filter(
                attributes__pk=pk2,
                product__id=pk,
            ).order_by('-id')
        serializer = ProductAttributesSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
def attribute_product_details(request):
    if request.method == 'POST':
        try:


            pk = request.data.get('product_id')
            pk2 = request.data.get('attributes_id')
            attribute = ProductAttributes.objects.get(
                attributes__pk=pk2,
                product__id=pk,
            )
        except ProductAttributes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductAttributesSerializer(
            attribute,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['PUT','POST','DELETE'])
def attribute_product(request):
    
    if request.method == 'POST':
        try:
            pk = request.data.get('attributes_id')
            attribute = Attributes.objects.get(
                pk=int(pk)
            )
        except Attributes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            pk = request.data.get('product_id')
            product = PostItem.objects.get(
                pk=int(pk)
            )
        except PostItem.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductAttributesSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(
                    product=product, 
                    attributes=attribute, 
                )
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )      
    if request.method == 'PUT' or request.method == 'DELETE':
        try:
            pk = request.data.get('id')
            product_attribute = ProductAttributes.objects.get(
                pk=int(pk)
            )
        except ProductAttributes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'PUT':
            serializer = ProductAttributesSerializer(
                product_attribute,
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data)

        if request.method == 'DELETE':
            product_attribute.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    
