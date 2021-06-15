from django.core.paginator import Paginator
from django.utils.text import slugify
from rest_framework import request, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from FunctionModule.cadastral.constants import district_data
from FunctionModule.listings.models import ListingSerializer
from FunctionModule.listings.search import prepare_listing_queryset


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


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def search_listing(req: request.Request, **kwargs):
    queryset_list = prepare_listing_queryset(req.query_params)

    try:
        page = int(req.query_params.get('page', 1))
    except ValueError:
        page = 1

    limit = req.query_params.get('limit', 10)
    offset = (page - 1) * limit
    paginator = Paginator(queryset_list, limit)
    total_pages = paginator.num_pages
    next_5_pages = page + 5 if page + 5 < total_pages else total_pages
    min_page = page - 1 if page - 1 > 0 else page

    try:
        listings = paginator.get_page(page)
    except Exception:
        listings = paginator.get_page(1)

    return response.Response({
        "listings": ListingSerializer(listings, many=True).data,
        # "listings": [],
        "pagination": {
            'current_page': page,
            'next_5_pages': list(range(min_page, next_5_pages)),
            'limit': limit,
            'offset': offset,
            'total': queryset_list.count()
        }
    })
