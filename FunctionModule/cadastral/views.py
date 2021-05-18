from rest_framework import request, response
from rest_framework.decorators import api_view

from .constants import state_data


@api_view(['GET'])
def get_states(r: request.Request):
    return response.Response(state_data)
