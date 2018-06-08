from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import InformationPost, Profile, User, Vote
from api.serializers import VoteSerializer
from utils.response import generate_response


@api_view(['GET', 'POST'])
def vote(request, id=None):

    if request.method == 'GET':

        upvotes = Vote.objects.filter(post=id, vote_type='upvote').count()
        downvotes = Vote.objects.filter(post=id, vote_type='downvote').count()

        data = {'upvotes': upvotes, 'downvotes': downvotes}

        return generate_response(data=data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)

        if Vote.objects.filter(post=id, voter=profile.id).count() > 0:
            return generate_response(message='You have already vote on this post',
                                     status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['voter'] = profile.id
        data['post'] = id
        data['weight'] = 1

        serializer = VoteSerializer(data=data)
        if not serializer.is_valid():
            return generate_response(message='Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return generate_response(data=serializer.data, status=status.HTTP_201_CREATED)

    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)
