
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from taxes.models import Taxes

class TaxesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxes
        fields =    (
            'id',
            'city',
            'country',
            'percent',
            'created', 
            'modified',
        )


@api_view(['GET'])
def taxes_list(request):
        
    if request.method == 'GET':
        media = Taxes.objects.all()
        serializer = TaxesSerializer(
            media, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
def taxes_create(request):
        
    if request.method == 'POST':
        serializer = TaxesSerializer(
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
def taxes_details(request):
    
    try:
        pk = request.data.get('id')
        tax = Taxes.objects.get(
            pk=int(pk)
        )
    except Taxes.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'POST':
        serializer = TaxesSerializer(
            tax,
            context={'request': request}
        )
        return Response(serializer.data)
    return Response(
            status=status.HTTP_204_NO_CONTENT
        )



@api_view(['DELETE','PUT','POST'])
def tax(request):
    if request.method in ['DELETE','PUT']:
        try:
            pk = request.data.get('id')
            tax = Taxes.objects.get(
                pk=int(pk)
            )
        except Taxes.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
    if request.method == 'DELETE':
        tax.delete()
    if request.method == 'POST':
        serializer = TaxesSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
 
    if request.method == 'PUT':
        serializer = TaxesSerializer(
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
