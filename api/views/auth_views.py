from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import Profile, create_user
from api.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def signin(request):

    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def signup(request):

    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)

        if not (username and password and email):
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)

        success = create_user(username=username, password=password, email=email)
        if not success:
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'success': True}, status=status.HTTP_201_CREATED)


# commented out while not used
# @api_view(['GET'])
# def userinfo(request, id):
#
#     if request.method == 'GET':
#         base_user = User.objects.filter(pk=id)
#
#         if not base_user:
#             return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = Profile.objects.filter(user=base_user[0])
#
#         if not user:
#             return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = UserSerializer(user[0])
#         return Response(serializer.data, status=status.HTTP_501_NOT_IMPLEMENTED)
