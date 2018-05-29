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


@api_view(['GET'])
def sendmail(request):
    mail_subject = '최경재바보'
    message = '최경재바보123'
    to = ['def6488@gmail.com']
    email = EmailMessage(
        mail_subject, message, to=to
    )
    email.send()
    return generate_response(message="Please confirm email", status=200)
