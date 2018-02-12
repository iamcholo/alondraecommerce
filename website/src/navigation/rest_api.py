from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from navigation.models import NavigationPosition
from django.contrib.auth.models import User
from navigation.models import NavigationItem
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_recursive.fields import RecursiveField

class NavigationPositionSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = NavigationPosition
        fields =    ('id', 'name','publish', 'created', 'modified',)


class NavigationItemSerializer(serializers.HyperlinkedModelSerializer):
 
     
    class Meta:
        model = NavigationItem
        fields =    ('id','item_id','view_name','title', 'created', 'modified','parent',)
    
    parent = serializers.ListField(read_only=True,child=RecursiveField(),source="get_descendants")
    title = serializers.SerializerMethodField('is_named_bar')
    item_id = serializers.SerializerMethodField('is_ided_bar')
    def is_named_bar(self, ob):
        if hasattr(ob.item, 'name'):
            return ob.item.name
        if hasattr(ob.item, 'title'):
            return ob.item.title
    def is_ided_bar(self, ob):        
        return ob.item.id
        
@api_view(['GET'])
def nav_list(request):
        
    if request.method == 'GET':
        navigation = NavigationPosition.objects.all()
        serializer = NavigationPositionSerializer(
            navigation, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST'])
def nav(request):
    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            navigation = NavigationPosition.objects.get(
                pk=pk
            )
        except NavigationPosition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = NavigationPositionSerializer(
            navigation,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

def getnav_item(nav):
    try:
        f1 = Q(app_label='posts')
        f2 = Q()
        if (nav.get('nav')=="category"):
            f2 = Q(model='PostCategory')
        if (nav.get('nav')=="post_details") or (nav.get('nav')=="page_details"):
            f2 = Q(model='PostItem')

        i = ContentType.objects.get(
            f1 & f2
            )
        return i.get_object_for_this_type(id=nav.get('id'))
                     
    except ObjectDoesNotExist:
        return None    

@api_view(['POST', 'PUT', 'DELETE'])
def nav_details(request):
    pk = request.data.get('id', None)
    navigations = request.data.get('navigation', [])
    
    if pk is not None:
        try:
            navigation = NavigationPosition.objects.get(
                pk=pk
            )
        except NavigationPosition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
     
    if request.method == 'POST':
        serializer = NavigationPositionSerializer(
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
    elif request.method == 'PUT':
        serializer = NavigationPositionSerializer(
            navigation, 
            data=request.data
        )
        if serializer.is_valid():
            print navigations
            serializer.save()
            NavigationItem.objects.filter(position__id=pk).delete() 
            items = NavigationItem.objects.filter(position__id=pk)
            if (len(items)==0):
                for nav in navigations:

                    i = getnav_item(nav)
                    
                    if i is not None:
                        cType = ContentType.objects.get_for_model(i)
                        parent, created = NavigationItem.objects.get_or_create(
                                    position=navigation,
                                    object_id=i.id,
                                    slug=i.slug,
                                    content_type=cType,
                                    view_name=nav.get('nav')
                                )
                        if (nav.has_key('children')):
                            for  children in nav.get('children'):
                                s = getnav_item(children)
                                if s is not None:
                                    cType = ContentType.objects.get_for_model(s)           
                                    child, created = NavigationItem.objects.get_or_create(
                                        parent=parent,
                                        position=navigation,
                                        object_id=s.id,
                                        slug=s.slug,
                                        content_type=cType,
                                        view_name=children.get('nav')
                                    )
                
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    
    if request.method == 'DELETE':
        navigation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def nav_item_list(request):
        
    if request.method == 'POST':
        pk = request.data.get('id')
        navigation = NavigationItem.objects.filter(
            parent=None,
            position__id=pk
        )
        serializer = NavigationItemSerializer(
            navigation, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST', 'PUT', 'DELETE'])
def nav_item_details(request):

    try:
        item = Navigation.objects.get(
            pk=request.data.get('id')
        )
    except Navigation.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )
 
    if request.method == 'POST':
        item_id = request.data.get("item_id", None)
        

        try:
            f1 = Q(app_label='posts')
            f2 = Q(model='PostCategory')
            f3 = Q(model='PostItem')
            i = ContentType.objects.get(
                f1 & (f2 | f3)
               )
            i.get_object_for_this_type(id=1)
        except ObjectDoesNotExist:
            pass
    return Response(status=status.HTTP_204_NO_CONTENT)
