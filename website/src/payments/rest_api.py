
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from payments.models import PaymentMethod,PaymentMethodFields


class PaymentMethodFieldsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentMethodFields
        fields =    (
            'id',
            'key',
            'value',
            'created', 
            'modified',
        )



class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):
    payment_info = serializers.SerializerMethodField('get_popularity')
    class Meta:
        model = PaymentMethod
        fields =    (
            'id',
            'payment_info',
            'amount',
            'currency',
            'payment_method',
            'created', 
            'modified',
        )

    def get_popularity(self, obj):
        request = self.context.get("request")
        posts = PaymentMethodFields.objects.filter(
                payment__id=obj.id,
            ).order_by('-id')
        serializer = PaymentMethodFieldsSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return serializer.data


@api_view(['GET'])
def payment_list(request):
        
    if request.method == 'GET':
        media = PaymentMethod.objects.all()
        serializer = PaymentMethodSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

@api_view(['POST'])
def payment_create(request):
        
    if request.method == 'POST':
        serializer = PaymentMethodSerializer(
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
def payment_details(request):
    
    try:
        pk = request.data.get('id')
        payment = PaymentMethod.objects.get(
            pk=int(pk)
        )
    except PaymentMethod.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'POST':
        serializer = TaxesSerializer(
            payment,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['DELETE','PUT','POST'])
def payment(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            payment = PaymentMethod.objects.get(
                pk=int(pk)
            )
        except PaymentMethod.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
    if request.method == 'DELETE':
        payment.delete()
    if request.method == 'POST':
        serializer = PaymentMethodSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
 
    if request.method == 'PUT':
        serializer = PaymentMethodSerializer(
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
