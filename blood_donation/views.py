__author__ = 'naveenkumar'

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def get_started(request):
    return Response(data={"status": 1}, status=status.HTTP_201_CREATED, content_type='application/json')

@api_view(['POST'])
def signup(request):
    pass

@api_view(['POST'])
def new_blood_req(request):
    pass

@api_view(['POST'])
def donor_response(request):
    pass

@api_view(['POST'])
def recipeint_feedback(request):
    pass