from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response
from api.serializers import QuestionPostSerializer, InformationPostSerializer
from api.models import QuestionPost, Profile, User, InformationPost
from django.utils.timezone import datetime


@swagger_auto_schema(methods=['get'], responses={200: QuestionPostSerializer})
@api_view(['GET'])
def questions(request):
    every_questions = QuestionPost.objects.all()
    serializer = QuestionPostSerializer(every_questions, many=True)

    # delete redundant field for list
    for x in serializer.data:
        x.pop('content', None)

    return generate_response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def questions_with_tag(request, tag):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def questions_with_type(request, type):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def questions_with_title(request, title):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@swagger_auto_schema(methods=['get'], responses={200: InformationPostSerializer})
@api_view(['GET'])
def informations(request):
    every_informations = InformationPost.objects.all()
    serializer = InformationPostSerializer(every_informations, many=True)

    # delete redundant field for list
    for x in serializer.data:
        x.pop('content', None)
        x.pop('hidden_content', None)

    return generate_response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def informations_with_tag(request, tag):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def informations_with_type(request, type):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def informations_with_title(request, title):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def all(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def all_with_tag(request, tag):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def all_with_type(request, type):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def all_with_title(request, title):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)
