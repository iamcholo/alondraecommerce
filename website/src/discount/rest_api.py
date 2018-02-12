
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import PostItem
from discount.models import Discounts

class DiscountsSerializer(serializers.HyperlinkedModelSerializer):
    product_pk = serializers.ReadOnlyField(source='product.id')
    class Meta:
        model = Discounts
        fields =    (
            'id',
            'product_pk',
            'percent',
            'start_date',
            'end_date',
            'created', 
            'modified',
        )


@api_view(['POST'])
def discounts_list(request):
        
    if request.method == 'POST':
        media = Discounts.objects.filter(
            product__pk=request.data.get(
                'product_id',
                None
            )
        )
        serializer = DiscountsSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
def discounts_create(request):
        
    if request.method == 'POST':
        serializer = DiscountsSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            try:
                pk = request.data.get('product_id')
                product = PostItem.objects.get(
                    pk=pk
                )
                serializer.save(
                    product=product
                )
                return Response(serializer.data)     
            except PostItem.DoesNotExist:
                 return Response(
                     status=status.HTTP_404_NOT_FOUND
                 )
             

            
    return Response(
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['POST'])
def discounts_details(request):
    
    try:
        pk = request.data.get('id')
        discount = Discounts.objects.get(
            pk=int(pk)
        )
    except Discounts.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'POST':
        serializer = DiscountsSerializer(
            discount,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['DELETE','PUT','POST'])
def discount(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            discount = Discounts.objects.get(
                pk=int(pk)
            )
        except Discounts.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
    if request.method == 'DELETE':
        discount.delete()


    if request.method == 'POST':
        serializer = DiscountsSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            try:
                pk = request.data.get('product_id')
                product = PostItem.objects.get(
                    pk=pk
                )
                serializer.save(
                    product=product
                )
                return Response(serializer.data)  
            except PostItem.DoesNotExist:
                 return Response(
                     status=status.HTTP_404_NOT_FOUND
                 )
                        
    if request.method == 'PUT':
        serializer = DiscountsSerializer(
            discount,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
          
            serializer.save()

            return Response(serializer.data)
        
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )
