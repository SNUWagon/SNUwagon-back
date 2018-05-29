from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import QuestionPostSerializer, InformationPostSerializer
from api.serializers import QuestionAnswerSerializer, BoughtInformationSerializer
from api.models import QuestionPost, Profile, User, InformationPost, QuestionAnswer
from api.models import BoughtInformation
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response


@api_view(['GET'])
def index(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@swagger_auto_schema(methods=['get'], responses={200: QuestionPostSerializer})
@swagger_auto_schema(methods=['post'], request_body=QuestionPostSerializer, responses={201: 'success'})
@swagger_auto_schema(methods=['delete'], responses={204: 'success'})
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
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
            return generate_response(message="error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    if request.method == 'PUT':
        try:
            qid = request.data['qid']
            aid = request.data['aid']
            question = QuestionPost.objects.get(pk=qid)
            answer = QuestionAnswer.objects.get(pk=aid)

            (question.resolved, question.selected) = (True, answer)
            question.save()

            cost = question.bounty

            question_writer = Profile.objects.get(pk=question.author.id)
            answer_writer = Profile.objects.get(pk=answer.author.id)

            question_writer.credit = question_writer.credit + (cost // 10)
            question_writer.save()
            answer_writer.credit = answer_writer.credit + cost
            answer_writer.save()
            return generate_response(message='Update successful', status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return generate_response(message="error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(methods=['get'], responses={200: QuestionAnswerSerializer})
@swagger_auto_schema(methods=['post'], request_body=QuestionAnswerSerializer, respnses={201: 'success'})
@api_view(['GET', 'POST'])
def answer(request, id=None):

    if request.method == 'GET':
        answers = QuestionAnswer.objects.filter(question=id)
        serializer = QuestionAnswerSerializer(answers, many=True)

        mutable_data = serializer.data.copy()
        for x in mutable_data:
            x['author'] = Profile.objects.get(pk=x['author']).user.username

        return generate_response(data=mutable_data, status=status.HTTP_200_OK)

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
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
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

            request_user = User.objects.get(username=request.user.username)
            request_profile = Profile.objects.get(user=request_user)
            mutable_data['hidden_bought'] = \
                BoughtInformation.objects.filter(user=request_profile, post=id).count() > 0
            return generate_response(mutable_data, status=status.HTTP_200_OK)

        except Exception as e:
            return generate_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        mutable_data = request.data.copy()

        user = User.objects.get(username=request.data['username'])
        profile = Profile.objects.get(user=user)
        mutable_data['author'] = profile.id

        if int(mutable_data['sponsor_credit']) > profile.credit:
            return generate_response(message='Not enough credits', status=status.HTTP_400_BAD_REQUEST)

        # Remove credit from user
        profile.credit -= int(mutable_data['sponsor_credit'])
        profile.save()

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

    if request.method == 'PUT':
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)
        information = InformationPost.objects.get(id=id)

        # Not enough Credit
        if information.hidden_content_cost > profile.credit:
            return generate_response(message='Not enough credits', status=status.HTTP_400_BAD_REQUEST)

        # Remove credit from user
        profile.credit -= int(information.hidden_content_cost)
        profile.save()

        mutable_data = {'user': profile.id, 'post': information.id}

        serializer = BoughtInformationSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return generate_response(message='Update successful', status=status.HTTP_200_OK)
        return generate_response(message='Unexpected error (Poke KJP)', status=status.HTTP_400_BAD_REQUEST)
