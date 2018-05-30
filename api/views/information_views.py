from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.serializers import InformationPostSerializer, BoughtInformationSerializer
from api.models import Profile, User, InformationPost, BoughtInformation
from django.db.utils import Error
from drf_yasg.utils import swagger_auto_schema
from utils.response import generate_response


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

        # Add credit to author
        information.author.credit = information.author.credit + information.hidden_content_cost
        information.author.save()

        mutable_data = {'user': profile.id, 'post': information.id}

        serializer = BoughtInformationSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return generate_response(message='Update successful', status=status.HTTP_200_OK)
        return generate_response(message='Unexpected error (Poke KJP)', status=status.HTTP_400_BAD_REQUEST)
