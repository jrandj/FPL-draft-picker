from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_data(request):
    message = {'name': 'Neil Breen', 'age': 60}
    return Response(message)
