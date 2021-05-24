from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from rest_framework import request, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from FunctionModule.cadastral.constants import district_data
from FunctionModule.listings.models import Listing, ListingSerializer


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
    queryset_list = Listing.objects.order_by('-list_date')
    hn_district = district_data['01']

    # Trantype
    if 'trantype' in req.query_params:
        trantype = req.query_params['trantype']
        if trantype:
            queryset_list = queryset_list.filter(transaction_type=trantype)

    # Housetype
    if 'housetype' in req.query_params:
        housetype = req.query_params['housetype'].split(',')
        if housetype:
            queryset_list = queryset_list.filter(house_type__in=housetype)

    # urban_area
    if 'urban_area' in req.query_params:
        urban_area = req.query_params['urban_area']
        if urban_area:
            queryset_list = queryset_list.filter(urban_area=urban_area)

    # Keywords
    if 'keywords' in req.query_params:
        keywords = req.query_params['keywords']
        if keywords:
            query = Q(description__icontains=keywords) | Q(name__icontains=keywords)
            queryset_list = queryset_list.filter(query)

            # Address
            if 'address' in req.query_params:
                address = req.query_params['address']
                if address:
                    queryset_list = queryset_list.filter(address=address)

        # street
        if 'street' in req.query_params:
            street = req.query_params['street']
            if street:
                queryset_list = queryset_list.filter(
                    Q(address__icontains=street) | Q(street__icontains=street))

    # District
    if 'district' in req.query_params:
        district = req.query_params['district']
        if district:
            district_code = next(x['code'] for x in hn_district if x['slug'] == district)
            if district_code:
                queryset_list = queryset_list.filter(district=district_code)

    # State
    if 'state' in req.query_params:
        state = req.query_params['state']
        if state:
            queryset_list = queryset_list.filter(state=state)

    # Bedrooms
    if 'bedrooms' in req.query_params:
        bedrooms = req.query_params['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'minPrice' in req.query_params:
        price = req.query_params['minPrice']
        if price:
            query = Q(price__gte=price)
            queryset_list = queryset_list.filter(query)
    if 'maxPrice' in req.query_params:
        max_price = req.query_params['maxPrice']
        if max_price:
            query = Q(price__lte=max_price)
            queryset_list = queryset_list.filter(query)

    # Area
    if 'minArea' in req.query_params:
        area = req.query_params['minArea']
        if area:
            query = Q(area__gte=area)
            queryset_list = queryset_list.filter(query)
    if 'maxArea' in req.query_params:
        area = req.query_params['maxArea']
        if area:
            query = Q(area__lte=area)
            queryset_list = queryset_list.filter(query)

    if 'sort' in req.query_params:
        sort_by = req.query_params.get('sort')
        if sort_by == 'price_ascend':
            queryset_list = queryset_list.order_by('price')
        elif sort_by == 'price_descend':
            queryset_list = queryset_list.order_by('-price')
        else:
            queryset_list = queryset_list.order_by('-list_date')

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
        "pagination": {
            'current_page': page,
            'next_5_pages': list(range(min_page, next_5_pages)),
            'limit': limit,
            'offset': offset,
            'total': queryset_list.count()
        }
    })
