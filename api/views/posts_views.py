from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import QuestionPostSerializer
from api.models import QuestionPost, Profile, User
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
def index(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@swagger_auto_schema(methods=['get', 'post'], request_body=QuestionPostSerializer)
@api_view(['GET', 'POST', 'DELETE'])
def question(request, id=None):

    if request.method == 'GET':
        try:
            question_object = QuestionPost.objects.get(pk=id)
            serializer = QuestionPostSerializer(question_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        mutable_data = request.data.copy()
        user = User.objects.get(username=request.data['user_name'])
        profile = Profile.objects.get(user=user)
        mutable_data['author'] = profile.id

        serializer = QuestionPostSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'POST'])
def information(request, id=None):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)
