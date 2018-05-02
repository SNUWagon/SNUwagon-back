from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['POST'])
def signin(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
def signup(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def userinfo(request, id):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)
