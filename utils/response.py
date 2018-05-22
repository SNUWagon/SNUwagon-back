from rest_framework.response import Response
from rest_framework import status as drf_status


def generate_response(data=None, message='', status=drf_status.HTTP_200_OK):

    if status in (drf_status.HTTP_200_OK, drf_status.HTTP_201_CREATED, drf_status.HTTP_204_NO_CONTENT):
        success = True
    else:
        success = False

    response = {
        'success': success,
    }

    if len(message) > 0:
        response.update({'message': message})

    if data:
        response.update({'data': data})
    else:
        response.update({'data': []})

    return Response(response, status=status)
