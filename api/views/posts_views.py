from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import QuestionPostSerializer, InformationPostSerializer, QuestionAnswerSerializer
from api.models import QuestionPost, Profile, User, InformationPost
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response


@api_view(['GET'])
def index(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@swagger_auto_schema(methods=['get'], responses={200: QuestionPostSerializer})
@swagger_auto_schema(methods=['post'], request_body=QuestionPostSerializer, responses={201: 'success'})
@swagger_auto_schema(methods=['delete'], responses={204: 'success'})
@api_view(['GET', 'POST', 'DELETE'])
def question(request, id=None):

    # Check user login
    if not request.user.is_authenticated:
        return generate_response(message='Not logged in', status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':

        try:
            question_object = QuestionPost.objects.get(pk=id)
            serializer = QuestionPostSerializer(question_object)

            # return author name for 'author' field
            mutable_data = serializer.data.copy()
            author = Profile.objects.get(pk=mutable_data['author'])
            mutable_data['author'] = author.user.username

            return generate_response(mutable_data, status=status.HTTP_200_OK)
        except Exception as e:
            return generate_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        mutable_data = request.data.copy()
        user = User.objects.get(username=request.data['username'])
        profile = Profile.objects.get(user=user)

        if int(mutable_data['bounty']) > profile.credit:
            return generate_response(message='Not enough credits', status=status.HTTP_400_BAD_REQUEST)

        mutable_data['author'] = profile.id
        mutable_data['resolved'] = False

        # Remove credit from user
        profile.credit -= int(mutable_data['bounty'])
        profile.save()

        serializer = QuestionPostSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return generate_response(data=serializer.data, status=status.HTTP_201_CREATED)

        return generate_response(message='Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':

        # Check if corresponding question exists
        results = QuestionPost.objects.filter(pk=id)
        if results.count() < 1:
            return generate_response(message='No such question found',
                                     status=status.HTTP_400_BAD_REQUEST)

        results.delete()
        return generate_response(message='Question deleted', status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['get'], responses={200: QuestionAnswerSerializer})
@swagger_auto_schema(methods=['post'], request_body=QuestionAnswerSerializer, respnses={201: 'success'})
@api_view(['GET', 'POST'])
def answer(request, id=None):

    if request.method == 'GET':
        # qid = id
        # question_object = QuestionPost.objects.get(pk=qid)

        return generate_response(message='Not Implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

    if request.method == 'POST':

        mutable_data = request.data.copy()

        mutable_data['question'] = mutable_data['qid']
        user = User.objects.get(username=request.data['username'])
        mutable_data['author'] = Profile.objects.get(user=user).id

        serializer = QuestionAnswerSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return generate_response(data=serializer.data, status=status.HTTP_201_CREATED)

        return generate_response(message='Invalid parameters', status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['get'], responses={200: InformationPostSerializer})
@swagger_auto_schema(methods=['post'], request_body=InformationPostSerializer, responses={201: 'success'})
@swagger_auto_schema(methods=['delete'], responses={204: 'success'})
@api_view(['GET', 'POST', 'DELETE'])
def information(request, id=None):

    # Check user login
    # if not request.user.is_authenticated:
    #    return generate_response(message='Not logged in', status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            information_object = InformationPost.objects.get(pk=id)
            serializer = InformationPostSerializer(information_object)

            # return author name for 'author' field
            mutable_data = serializer.data.copy()
            author = Profile.objects.get(pk=mutable_data['author'])
            mutable_data['author'] = author.user.username

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
            return generate_response(data=serializer.data, status=status.HTTP_201_CREATED)
        return generate_response(message='Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':

        # Check if corresponding information exists
        results = InformationPost.objects.filter(pk=id)
        if results.count() < 1:
            return generate_response(message='No such information found',
                                     status=status.HTTP_400_BAD_REQUEST)

        results.delete()
        return generate_response(message='Information deleted', status=status.HTTP_200_OK)
