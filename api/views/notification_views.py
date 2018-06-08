from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import NotificationSerializer
from api.models import Notification, Profile, User
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response


def generate_notification(profile_id, notification_type, content_id, message):
    notification_data = {
        'profile': profile_id,
        'notification_type': notification_type,
        'content_id': content_id,
        'message': message
    }
    notification_serializer = NotificationSerializer(data=notification_data)
    if notification_serializer.is_valid():
        notification_serializer.save()
    else:
        print(notification_serializer.errors)


@api_view(['GET'])
def notification(request):

    # Check user login
    if not request.user.is_authenticated:
        return generate_response(message='Not logged in', status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)

        every_notifications = Notification.objects.filter(profile=profile, pushed=False)
        serializer = NotificationSerializer(every_notifications, many=True)

        response = generate_response(serializer.data, status=status.HTTP_200_OK)

        every_notifications.update(pushed=True)

        return response


@api_view(['GET', 'PUT'])
def newsfeed(request):

    # Check user login
    if not request.user.is_authenticated:
        return generate_response(message='Not logged in', status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)

        every_notifications = Notification.objects.filter(profile=profile, read=False)
        serializer = NotificationSerializer(every_notifications, many=True)

        response = generate_response(serializer.data, status=status.HTTP_200_OK)

        every_notifications.update(pushed=True)

        return response

    if request.method == 'PUT':
        nid = request.data['nid']
        notification = Notification.objects.get(id=nid)
        notification.read = True
        notification.save()

        return generate_response(status=status.HTTP_200_OK)


@api_view(['POST'])
def watchtags(request):

    # Check user login
    if not request.user.is_authenticated:
        return generate_response(message='Not logged in', status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)
        profile.watch_tags = request.data['tags']
        profile.save()

        return generate_response(status=status.HTTP_200_OK)
