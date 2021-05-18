from django.utils.text import slugify
from rest_framework import request, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from FunctionModule.cadastral.constants import district_data


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_states(r: request.Request, **kwargs):
    query = kwargs.get('lookup', '')
    action = kwargs.get('action', 'sell')
    hn_district = district_data['01']
    query = slugify(query.lower().replace('đ', 'd').replace('õ', 'o'))
    query = query.split('-')
    records = []
    for item in hn_district:
        for q in query:
            if q in item['slug']:
                records.append(item)
                break
    data = [
        {"type": "area", "records": records}
    ]
    return response.Response(data)
