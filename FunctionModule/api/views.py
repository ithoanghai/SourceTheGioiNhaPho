import math

from django.core.paginator import Paginator
from rest_framework import request, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from FunctionModule.listings.models import ListingSerializer
from FunctionModule.listings.search import prepare_listing_queryset, search_by_keywords, get_suggestions


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_states(r: request.Request, **kwargs):
    query = kwargs.get('lookup', '')
    action = kwargs.get('action', 'sell')
    data = get_suggestions(query)
    return response.Response(data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def search_listing(req: request.Request, **kwargs):
    try:
        page = int(req.query_params.get('page', 1))
    except ValueError:
        page = 1

    previous_page = None if page == 1 else page - 1
    limit = req.query_params.get('limit', 10)
    offset = (page - 1) * limit
    min_page = page - 1 if page - 1 > 0 else page

    keywords = req.query_params.get('keywords', '')
    if keywords:
        results = search_by_keywords(keywords, limit, offset)
        total: int = results['nbHits']
        total_pages = int(math.ceil(total / limit))
        next_page = page + 1 if total_pages > page else None
        next_5_pages = list(range(min_page, page + 5 if page + 5 < total_pages else total_pages))
        next_5_pages = next_5_pages if len(next_5_pages) > 1 else [page]

        return response.Response({
            'listings': results['hits'],
            'pagination': {
                'current_page': page,
                'previous_page': previous_page,
                'next_page': next_page,
                'next_5_pages': next_5_pages,
                'limit': limit,
                'offset': offset,
                'total': results['nbHits']
            }
        })

    queryset_list = prepare_listing_queryset(req.query_params)
    paginator = Paginator(queryset_list, limit)
    total_pages = paginator.num_pages
    next_page = page + 1 if total_pages > page else None
    next_5_pages = list(range(min_page, page + 5 if page + 5 < total_pages else total_pages))
    next_5_pages = next_5_pages if len(next_5_pages) > 1 else [page]

    try:
        listings = paginator.get_page(page)
    except Exception:
        listings = paginator.get_page(1)

    return response.Response({
        "listings": ListingSerializer(listings, many=True).data,
        # "listings": [],
        "pagination": {
            'current_page': page,
            'previous_page': previous_page,
            'next_page': next_page,
            'next_5_pages': next_5_pages,
            'limit': limit,
            'offset': offset,
            'total': queryset_list.count()
        }
    })
