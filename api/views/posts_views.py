from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
def index(request):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'POST', 'DELETE'])
def question(request, id=None):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'POST'])
def information(request, id=None):
    return Response({'message': 'NOT IMPLEMENTED'}, status=status.HTTP_501_NOT_IMPLEMENTED)
