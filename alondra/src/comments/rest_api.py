
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from comments.models import Comments

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
