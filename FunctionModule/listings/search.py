from django.db.models import Q
from django.utils.text import slugify

from .models import Listing
from ..cadastral.constants import district_data


def prepare_listing_queryset(input_params):
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)
    hn_district = district_data['01']

    # trans_type
    if 'trans_type' in input_params:
        trans_type = input_params.get('trans_type')
        if trans_type:
            queryset_list = queryset_list.filter(transaction_type=trans_type)

    # Housetype
    if 'housetype' in input_params:
        housetype = input_params.get('housetype').split(',')
        if housetype:
            queryset_list = queryset_list.filter(house_type__in=housetype)

    # urban_area
    if 'urban_area' in input_params:
        urban_area = input_params.get('urban_area')
        if urban_area:
            queryset_list = queryset_list.filter(urban_area=urban_area)

    # Keywords
    if 'keywords' in input_params:
        keywords = input_params.get('keywords')
        if keywords:
            query = Q(description__icontains=keywords) | Q(title__icontains=keywords) | Q(
                address__icontains=keywords) | Q(code=keywords)
            slug_keyword = slugify(keywords.lower().replace('đ', 'd').replace('õ', 'o'))
            district_code = next(
                x['code'] for x in hn_district if
                (x['name'] == keywords or x['slug'] == slug_keyword or x['code'] == slug_keyword))
            if district_code:
                query = query | Q(district=district_code)
            queryset_list = queryset_list.filter(query)

            # Address
            if 'address' in input_params:
                address = input_params.get('address')
                if address:
                    queryset_list = queryset_list.filter(address=address)

    # street
    if 'street' in input_params:
        street = input_params.get('street')
        if street:
            queryset_list = queryset_list.filter(
                Q(address__icontains=street) | Q(street__icontains=street))

    # District
    if 'district' in input_params:
        district = input_params.get('district')
        if district:
            district_code = next(
                x['code'] for x in hn_district if x['slug'] == district or x['code'] == district)
            if district_code:
                queryset_list = queryset_list.filter(district=district_code)

    # State
    if 'state' in input_params:
        state = input_params.get('state')
        if state:
            queryset_list = queryset_list.filter(state=state)

    ward = input_params.get('ward', None)
    if ward:
        queryset_list = queryset_list.filter(ward=ward)

    # Bedrooms
    if 'bedrooms' in input_params:
        bedrooms = input_params.get('bedrooms')
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'minPrice' in input_params:
        price = input_params.get('minPrice')
        if price:
            query = Q(price__gte=price)
            queryset_list = queryset_list.filter(query)
    if 'maxPrice' in input_params:
        max_price = input_params.get('maxPrice')
        if max_price:
            query = Q(price__lte=max_price)
            queryset_list = queryset_list.filter(query)

    # Area
    if 'minArea' in input_params:
        area = input_params.get('minArea')
        if area:
            query = Q(area__gte=area)
            queryset_list = queryset_list.filter(query)
    if 'maxArea' in input_params:
        area = input_params.get('maxArea')
        if area:
            query = Q(area__lte=area)
            queryset_list = queryset_list.filter(query)

    if 'sort' in input_params:
        sort_by = input_params.get('sort')
        if sort_by == 'price_ascend':
            queryset_list = queryset_list.order_by('price')
        elif sort_by == 'price_descend':
            queryset_list = queryset_list.order_by('-price')
        else:
            queryset_list = queryset_list.order_by('-list_date')

    return queryset_list
