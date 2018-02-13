from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from orders.models import Orders,OrderShippingItem
from user_addresses.rest_api import AddresessSerializer
from django.contrib.auth.models import User
from user.rest_api import UserSerializer
from payments.rest_api import PaymentMethodSerializer
from user_addresses.rest_api import AddresessSerializer
from posts.rest_api import PostItemSerializer
from utilities.paginator import paginator

class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    billing_addresssx = AddresessSerializer(source='billing_addresss',many=False, read_only = True)
    shipping_addressx = AddresessSerializer(source='shipping_addresss',many=False, read_only = True) 
    payment_methodx = PaymentMethodSerializer(source='payment_method',many=False, read_only = True)   
    autorx = UserSerializer(source='autor',many=False, read_only = True)  
    order_id = serializers.SerializerMethodField('my_order_id')

    def my_order_id(self, obj):
        return str(obj.id).zfill(15)
    class Meta:
        model = Orders
        fields =    (
            'id',
            'status',
            'order_id',
            'autorx',
            'payment_methodx',
            'billing_addresssx',
            'shipping_addressx',
            'created', 
            'modified',
        )

class OrderShippingItemSerializer(serializers.HyperlinkedModelSerializer):
    order_ids = serializers.ReadOnlyField(source='order.id')
    productx = PostItemSerializer(source='product',read_only = True)
    class Meta:
        model = OrderShippingItem
        fields =    (
            'id',
            'order_ids',
            'productx',
            'price',
            'qty',
            #'status',
            'carrier',
            'tracking_number',
            'created', 
            'modified',
        )


@api_view(['POST'])
def order_list(request):

    if request.method == 'POST':
        page = int(request.data.get('page',1))
        media = paginator(
                page, 
                Orders.objects.all(),
                100
            )
        next_page = 0
        previous_page = 0
        if media.has_next():
            next_page = media.next_page_number()
        if media.has_previous():
            previous_page = media.previous_page_number()
                   
        serializer = OrdersSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response({
            'pages':media.paginator.num_pages,
            'items':serializer.data,
            'next_page':next_page,
            'previous_page':previous_page,
        })

@api_view(['DELETE','PUT','POST'])
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

@api_view(['POST'])
def order_details(request):
    if request.method == 'POST':
        try:
            pk = request.data.get('id')
            order = Orders.objects.get(
                pk=pk
            )
        except Orders.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrdersSerializer(
            order,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )


@api_view(['POST'])
def order_shipping_item_list(request):
        
    if request.method == 'POST':
        pk = request.data.get('id')
        order_shipping_items = OrderShippingItem.objects.filter(order__pk=pk)
        serializer = OrderShippingItemSerializer(
            order_shipping_items, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['DELETE','PUT','POST'])
def order_shipping_item(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            order_shipping = OrderShippingItem.objects.get(
                pk=int(pk)
            )
        except OrderShippingItem.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
    if request.method == 'DELETE':
        order_shipping.delete()
    if request.method == 'POST':
        serializer = OrdersSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
 
    if request.method == 'PUT':
        serializer = OrderShippingItemSerializer(
            order_shipping,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )