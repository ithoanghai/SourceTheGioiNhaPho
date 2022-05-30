import csv
import math
import os
import tempfile
from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from rest_framework import request, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from FunctionModule.listings.export_csv import prepare_fb_headers, prepare_fb_listing_data
from FunctionModule.listings.models import ListingSerializer, Listing
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_user(r: request.Request, **kwargs):

    return response.Response({
        "username": r.user.username,
        "can_export_listing": r.user.is_superuser,
        "can_import_listing": r.user.is_superuser,
    })


def query_params_to_filters(input_params):
    query = []

    is_verified = input_params.get('is_verified', None)
    if is_verified:
        query.append(['is_verified=true'])

    is_exclusive = input_params.get('is_exclusive', None)
    if is_exclusive:
        query.append(['is_exclusive=true'])

    # Status: List
    status: str = input_params.get('status', None)
    if status:
        statuses = status.split(',')
        if len(statuses):
            st_query = [f'status={s}' for s in statuses]
            query.append(st_query)

    # Directions: List
    directions = input_params.get('directions', None)
    if directions:
        directions = directions.split(',')
        if len(directions):
            direction_query = [f'status={s}' for s in directions]
            query.append(direction_query)

    # House type: List
    house_type = input_params.get('house_type', None)
    if house_type:
        house_type = house_type.split(',')
        if len(house_type):
            ht_query = [f'status={s}' for s in house_type]
            query.append(ht_query)

    # Bedrooms: List
    bedrooms = input_params.get('bedrooms', None)
    if bedrooms:
        bedrooms = bedrooms.split(',')
        to_filter = []
        for f in bedrooms:
            if f == '6+':
                to_filter.append('bedrooms>=6')
            else:
                to_filter.append(f'bedrooms={f}')
        if len(to_filter):
            query.append(to_filter)

    # Bathrooms: Single string
    bathrooms = input_params.get('bathrooms', None)
    if bathrooms:
        if bathrooms == 'all':
            pass
        elif bathrooms == '5+':
            query.append(['bathrooms>=5'])
        else:
            query.append([f'bathrooms={bathrooms}'])

    # Price: minPrice and maxPrice each single number
    price = input_params.get('minPrice', None)
    if price and price.isnumeric():
        query.append([f'price>={price}'])
    max_price = input_params.get('maxPrice', None)
    if max_price and max_price.isnumeric():
        query.append([f'price<{max_price}'])

    # Area: minArea and maxArea each single number
    area = input_params.get('minArea')
    if area and area.isnumeric():
        query.append([f'area>={area}'])
    max_area = input_params.get('maxArea')
    if max_area and max_area.isnumeric():
        query.append([f'area>={max_area}'])

    if 'sort' in input_params:
        sort_by = input_params.get('sort')

    return query


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def search_listing(req: request.Request, **kwargs):
    try:
        page = int(req.query_params.get('page', 1))
    except ValueError:
        page = 1

    previous_page = None if page == 1 else page - 1
    limit = req.query_params.get('limit', 50)
    offset = (page - 1) * limit
    min_page = page - 1 if page - 1 > 0 else page

    # keywords = req.query_params.get('keywords', '')
    # if keywords:
    #     filters = query_params_to_filters(req.query_params)
    #     results = search_by_keywords(keywords, limit, offset, filters)
    #     total: int = results['nbHits']
    #     total_pages = int(math.ceil(total / limit))
    #     next_page = page + 1 if total_pages > page else None
    #     next_5_pages = list(range(min_page, page + 5 if page + 5 < total_pages else total_pages))
    #     next_5_pages = next_5_pages if len(next_5_pages) > 1 else [page]
    #
    #     return response.Response({
    #         'listings': results['hits'],
    #         'pagination': {
    #             'current_page': page,
    #             'previous_page': previous_page,
    #             'next_page': next_page,
    #             'next_5_pages': next_5_pages,
    #             'limit': limit,
    #             'offset': offset,
    #             'total': results['nbHits']
    #         }
    #     })

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


@api_view(['POST'])
@csrf_protect
def download_exported_listing(req: request.Request, **kwargs):
    file_path = os.path.join(tempfile.gettempdir(), 'tmp.csv')
    with open(file_path, 'w', encoding='utf-8') as fp:
        headers = prepare_fb_headers()
        writer = csv.DictWriter(fp, fieldnames=headers)
        writer.writeheader()
        for listing in Listing.objects.all():
            listing_data = prepare_fb_listing_data(listing)
            writer.writerow(listing_data)
    with open(file_path, 'r', encoding='utf-8') as fp:
        resp = HttpResponse(fp.read(), content_type="text/csv")
        resp['Content-Disposition'] = f'filename=tgnp_bds_facebook_export-{datetime.today().strftime("%Y-%m-%d")}.csv'
        return resp