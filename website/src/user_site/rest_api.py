import json
import random
import hashlib
from django.conf import settings
from user.models import CustomUser as User 
from rest_framework import routers, serializers, viewsets, generics
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from utilities.send_email import send_mail
from user_site.rest_authentication import UserSiteIsAuthenticated
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model,authenticate, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields =    (
            'id', 
            'first_name',
            'last_name', 
            'is_active',
            'is_superuser',
            'username', 
            'email',
            'nick', 
            #'created', 
            #'modified',
        )



class UserSecrectQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'security_answer',
            'security_question',
            #'created',
            #'modified',
        )

class UserPasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'password',           
            #'created',
            #'modified',
        )


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    data = {'success': False}
    if request.method == 'POST':
        user_cache = authenticate(
                username=username,
                password=password
            )

        if user_cache is not None: 
            auth_login(request, user_cache)
        data = {'success': request.user.is_authenticated()}
    return Response(
            data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes((UserSiteIsAuthenticated,))
def user_list(request):
        
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(
            users, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST'])
def logout(request):

    data = {'success': False}
    if request.method == 'POST':
        auth_logout(request)
        data = {'success': request.user.is_authenticated() == False}
    return Response(
            data,
            status=status.HTTP_201_CREATED
        )


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes((UserSiteIsAuthenticated,))
def user_details(request):

    try:
        user = User.objects.get(
            pk=request.data.get('id')
        )
    except User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )
 
    if request.method == 'POST':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(
            user, 
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT'])
@permission_classes((UserSiteIsAuthenticated,))
def user(request):

    try:
        pk = request.data.get('id') or request.user.id
        user = User.objects.get(
            pk=pk
        )
    except User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )
 
    if request.method == 'GET':
        serializer = UserSerializer(user)   
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(
            user, 
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )    

@api_view(['PUT'])
@permission_classes((UserSiteIsAuthenticated,))
def user_udpate_password(request):

    try:
        pk = request.data.get('id') or request.user.id
        user = User.objects.get(
            pk=pk
        )
    except User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )
    #user.set_password(request.data.get('new_password'))
    if request.method == 'PUT':
        old_password =  request.data.get("old_password")
        if not request.user.check_password(old_password):
            message = _("Your old password was entered incorrectly. Please enter it again.")
            res = {
                "code": 400, 
                "message": unicode(message),
            }
            return Response(
                    data=res,                
                    status=status.HTTP_200_OK
                )
        password1 = request.data.get('new_password')
        password2 = request.data.get('repeat_new_password')
        if password1 and password2:
            if password1 != password2:
                message = _("The two password fields didn't match.")           
                res = {
                    "code": 400, 
                    "message": unicode(message),
                }
                return Response(
                    data=res,                
                    status=status.HTTP_200_OK
                )
            else:
                user.set_password(request.data.get('new_password'))

        
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes((UserSiteIsAuthenticated,))
def user_create(request):
    if request.method == 'POST':
        user = User.objects.filter(
                    email=request.data.get('email')
                )
        if len(user) == 0:
            serializer = UserSerializer(
                data=request.data, 
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                try:
                    user = User.objects.get(
                        id=serializer.data.get('id')
                    )
                    user.set_password(request.data.get('password'))
                    user.save()
                except User.DoesNotExist:
                    return Response(
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                return Response(serializer.data)
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )            



@api_view(['GET'])
def check_online(request):
    if request.method == 'GET':
        
        return Response({
            'logged': request.user.is_authenticated()
        })
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['PUT',])
@permission_classes((UserSiteIsAuthenticated,))
def delete_user(request):
    if request.method == 'PUT':
        pk = request.data.get('id')
        User.objects.filter( pk=pk).delete()
            
    return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['PUT',])
@permission_classes((UserSiteIsAuthenticated,))
def delete_user(request):
    if request.method == 'PUT':
        pk = request.data.get('id')
        User.objects.filter( pk=pk).delete()
            
    return Response(status=status.HTTP_204_NO_CONTENT)
    
    
        
