from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import Profile, create_user
from api.serializers import UserSerializer, UserProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response
from django.core.mail import EmailMessage
from hashlib import md5
import string
import random
from django.shortcuts import redirect


@swagger_auto_schema(methods=['post'], request_body=UserSerializer, responses={201: 'success'})
@api_view(['POST'])
def signin(request):

    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if User.objects.filter(username=username).count() == 0:
            return generate_response(message='Username or password is wrong', status=status.HTTP_401_UNAUTHORIZED)

        profile = Profile.objects.get(user=User.objects.get(username=username))
        if profile.verified is False:
            return generate_response(message='Please verify email first', status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return generate_response(status=status.HTTP_200_OK)
        else:
            return generate_response(message='Username or password is wrong', status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(methods=['post'], request_body=UserSerializer, responses={201: 'success'})
@api_view(['POST'])
def signup(request):

    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)

        if not (username and password and email):
            return generate_response(message='Parameters are not given', status=status.HTTP_401_UNAUTHORIZED)

        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        salted_username = username
        for i in range(5):
            salted_username = salted_username + random.choice(ALPHABET)
        hashstring = md5(salted_username.encode()).hexdigest()

        success = create_user(username=username, password=password, email=email, hashstring=hashstring)
        if not success:
            return generate_response(message='Duplicate username or email', status=status.HTTP_401_UNAUTHORIZED)

        mail_subject = '[SNUWagon] Please confirm your email'
        message = 'http://www.snuwagon.com:8000/api/auth/verification/' + hashstring
        to = [email]
        email = EmailMessage(
            mail_subject, message, to=to
        )
        email.send()

        return generate_response(message='Please authenticate email', status=status.HTTP_201_CREATED)


@api_view(['GET'])
def verification(request, hashstring):

    profile = Profile.objects.get(hashstring=hashstring)
    profile.verified = True
    profile.save()
    return redirect('http://www.snuwagon.com:3000/')


@swagger_auto_schema(methods=['get'], responses={200: 'success'})
@api_view(['GET'])
def signout(request):

    if request.method == 'GET':
        logout(request)
        return generate_response(status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['get'], responses={200: UserProfileSerializer})
@api_view(['GET'])
def userinfo(request, id=None):

    if request.method == 'GET':
        if not id:
            id = request.user.id

        base_user = User.objects.filter(pk=id)

        if not base_user:
            return generate_response(message="No such user", status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(base_user[0])
        return generate_response(serializer.data, status=status.HTTP_200_OK)
