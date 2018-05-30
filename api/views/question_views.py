from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import QuestionPostSerializer, QuestionAnswerSerializer
from api.models import QuestionPost, Profile, User, QuestionAnswer
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response


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
