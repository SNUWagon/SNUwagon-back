from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import QuestionPostSerializer, InformationPostSerializer
from api.models import QuestionPost, Profile, User, InformationPost
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response


@api_view(['GET'])
def index(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@swagger_auto_schema(methods=['get'], responses={200: QuestionPostSerializer})
@swagger_auto_schema(methods=['post'], request_body=QuestionPostSerializer, responses={201: 'success'})
@api_view(['GET', 'POST', 'DELETE'])
def question(request, id=None):

    if request.method == 'GET':
        try:
            question_object = QuestionPost.objects.get(pk=id)
            serializer = QuestionPostSerializer(question_object)
            return generate_response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return generate_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        mutable_data = request.data.copy()
        user = User.objects.get(username=request.data['username'])
        profile = Profile.objects.get(user=user)
        mutable_data['author'] = profile.id

        serializer = QuestionPostSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return generate_response(status=status.HTTP_201_CREATED)

        return generate_response(message='Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@swagger_auto_schema(methods=['get'], responses={200: InformationPostSerializer})
@swagger_auto_schema(methods=['post'], request_body=InformationPostSerializer, responses={201: 'success'})
@api_view(['GET', 'POST'])
def information(request, id=None):

    if request.method == 'GET':
        try:
            information_object = InformationPost.objects.get(pk=id)
            serializer = InformationPostSerializer(information_object)
            return generate_response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return generate_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        mutable_data = request.data.copy()
        user = User.objects.get(username=request.data['username'])
        profile = Profile.objects.get(user=user)
        mutable_data['author'] = profile.id
        serializer = InformationPostSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return generate_response(status=status.HTTP_201_CREATED)
        return generate_response(message='Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)
