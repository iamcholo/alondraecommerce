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


class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    billing_addresss_ids = AddresessSerializer(source='billing_addresss.id', read_only = True)
    shipping_addresss_ids = AddresessSerializer(source='shipping_addresss.id', read_only = True) 
    payment_method_ids = PaymentMethodSerializer(source='payment_method.id', read_only = True)   
    autor_ids = UserSerializer(source='autor.id', read_only = True)  
    order_id = serializers.SerializerMethodField('my_order_id')

    def my_order_id(self, obj):
        return str(obj.id).zfill(15)
    class Meta:
        model = Orders
        fields =    (
            'id',
            'status',
            'order_id',
            'autor_ids',
            'payment_method_ids',
            'billing_addresss_ids',
            'shipping_addresss_ids',
            'created', 
            'modified',
        )

class OrderShippingItemSerializer(serializers.HyperlinkedModelSerializer):
    order_ids = serializers.ReadOnlyField(source='order.id')
    product_ids = serializers.ReadOnlyField(source='product.id')
    class Meta:
        model = OrderShippingItem
        fields =    (
            'id',
            'order_ids',
            'product_ids',
            'value',
            'price',
            'status',
            'carrier',
            'tracking_number',
            'created', 
            'modified',
        )


@api_view(['GET'])
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
        order_shipping_items = OrderShippingItem.objects.filter(order_pk=pk)
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