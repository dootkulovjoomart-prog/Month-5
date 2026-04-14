from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .seriializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def registration_api_view(request):
    serializers = RegisterSerializer(data = request.data)
    serializers.is_valid(raise_exception=True)

    username = serializers.validated_data.get('username')
    password = serializers.validated_data.get('password')

    user = User.objects.create_user(
            username=username,
            password=password,
            is_active = True

    )

    return Response(
        status=status.HTTP_201_CREATED , 
        data={'user_id':user.id}
    )

@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')


    user = authenticate(username = username , password = password)  
    if user is not None:
        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        return Response(data={'key' : token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)

