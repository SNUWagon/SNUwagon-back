from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import Profile, create_user
from api.serializers import UserSerializer, UserProfileSerializer
from utils.response import generate_response
from django.test.utils import override_settings
from django.conf import settings


@api_view(['GET'])
def verify(request, username):

    if request.method == 'GET':
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profile.verified = True
        if settings.DEBUG:
            profile.save()
        return generate_response(status=status.HTTP_200_OK)


@api_view(['GET'])
def credit(request, username):

    if request.method == 'GET':
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profile.credit = profile.credit + 1000
        if settings.DEBUG:
            profile.save()
        return generate_response(status=status.HTTP_200_OK)
