from django.db.models import Q
from django.utils.text import slugify

from TownhouseWorldRealestate.search_engine import listing_search, suggestions_search
from .models import Listing
from ..cadastral.constants import district_data
from ..cadastral.lookups import get_district, get_state, get_state_name, get_ward


def search_by_keywords(q: str, limit: int = 50, offset: int = 0, filters=None):
    if not q:
        return []

    search_dict = {
        'limit': limit,
        'offset': offset,
    }
    if filters:
        search_dict['filter'] = filters

    results = listing_search.search(q, search_dict)
    return results


def get_suggestions(q: str, limit: int = 50, offset: int = 0, ):
    if not q:
        return []
    try:
        results = suggestions_search.search(q, {
            'limit': limit,
            'offset': offset
        })
        return results["hits"]
    except Exception as e:
        print(e)
        return []


def prepare_listing_queryset(input_params):
    queryset_list = Listing.objects.order_by('priority','-date_created').filter(is_published=True)
    hn_district = district_data['01']

    # trans_type
    if 'trans_type' in input_params:
        trans_type = input_params.get('trans_type')
        if trans_type:
            queryset_list = queryset_list.filter(transaction_type=trans_type)
    #check listing is post
    if 'advertising' in input_params:
        is_advertising = input_params.get('advertising', None)
        if is_advertising:
            queryset_list = queryset_list.filter(is_advertising=bool(is_advertising))
    else:
        queryset_list = queryset_list.filter(is_advertising=bool(False))

    is_verified = input_params.get('is_verified', None)
    if is_verified:
        queryset_list = queryset_list.filter(is_verified=bool(is_verified))

    is_exclusive = input_params.get('is_exclusive', None)
    if is_exclusive:
        queryset_list = queryset_list.filter(is_exclusive=bool(is_exclusive))

    status = input_params.get('status', None)
    if status:
        statuses = status.split(',')
        queryset_list = queryset_list.filter(status__in=statuses)

    directions = input_params.get('directions', None)
    if directions:
        directions = directions.split(',')
        queryset_list = queryset_list.filter(direction__in=directions)

    house_type = input_params.get('house_type', None)
    if house_type:
        ht = house_type.split(',')
        queryset_list = queryset_list.filter(house_type__in=ht)

    if 'urban_area' in input_params:
        urban_area = input_params.get('urban_area')
        if urban_area:
            queryset_list = queryset_list.filter(urban_area__in=urban_area)

    # Keywords
    if 'keywords' in input_params:
        keywords = input_params.get('keywords')
        if keywords:
            query = Q(address__icontains=keywords) | Q(street__icontains=keywords) | Q(code__icontains= keywords)
            queryset_list = queryset_list.filter(query)
    # District
    if 'street' in input_params:
        street = input_params.get('street')
        if street:
            queryset_list = queryset_list.filter(address__in=street, street__in=street)

    # District
    if 'district' in input_params:
        district = input_params.get('district')
        if district:
            district_code = next(
                x['code'] for x in hn_district if x['slug'] == district or x['code'] == district)
            if district_code:
                queryset_list = queryset_list.filter(district=district_code)

    # State
    state = input_params.get('state')
    if state:
        queryset_list = queryset_list.filter(state=state)

    ward = input_params.get('ward', None)
    if ward:
        queryset_list = queryset_list.filter(ward=ward)

    # Bedrooms
    bedrooms = input_params.get('bedrooms', None)
    if bedrooms:
        bedrooms = bedrooms.split(',')
        to_filter = []
        filter_over_6 = False
        for f in bedrooms:
            if f == '6+':
                filter_over_6 = True
            else:
                to_filter.append(f)
        query = Q(bedrooms__in=to_filter)
        if filter_over_6:
            query = query | Q(bedrooms__gte=6)
        queryset_list = queryset_list.filter(query)

    bathrooms = input_params.get('bathrooms', None)
    if bathrooms:
        if bathrooms == 'all':
            pass
        elif bathrooms == '5+':
            queryset_list = queryset_list.filter(bathrooms__gte=5)
        else:
            queryset_list = queryset_list.filter(bathrooms=bathrooms)

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
    area = input_params.get('minArea')
    if area and area.isnumeric():
        query = Q(area__gte=area)
        queryset_list = queryset_list.filter(query)
    max_area = input_params.get('maxArea')
    if max_area and max_area.isnumeric():
        query = Q(area__lte=max_area)
        queryset_list = queryset_list.filter(query)

    if 'sort' in input_params:
        sort_by = input_params.get('sort')
        if sort_by == 'price_ascend':
            queryset_list = queryset_list.order_by('price')
        elif sort_by == 'price_descend':
            queryset_list = queryset_list.order_by('-price')
        elif sort_by == 'created':
            queryset_list = queryset_list.order_by('-date_created')
        else:
            queryset_list = queryset_list.order_by('priority')

    return queryset_list

def prepare_index_from_listing(listing):
    suggestions_data = []
    street = listing.street
    district = get_district(listing.district)
    street_id = slugify(f'{street} {district["path"]}'.lower().replace('đ', 'd').replace('õ', 'o'))
    suggestions_data.append({
        "id": street_id,
        "type": 'street',
        'sub_type': '',
        "text": street,
        "sub_text": district['path'],
    })
    state = get_state(listing.state)
    suggestions_data.append({
        "id": state['code'],
        "type": 'area',
        'sub_type': 'state',
        "text": state['name'],
        "sub_text": '',
    })
    suggestions_data.append({
        "id": district['code'],
        "type": 'area',
        'sub_type': 'district',
        "text": district['name'],
        "sub_text": get_state_name(district['parent_code'])
    })
    if listing.urban_area:
        suggestions_data.append({
            "id": slugify(f"{state['name']}-{listing.urban_area}"
                          .lower().replace('đ', 'd').replace('õ', 'o')),
            "type": 'urban_area',
            'sub_type': '',
            'text': listing.urban_area,
            'sub_text': district['path'],
        })

    if listing.ward:
        ward = get_ward(listing.district, listing.ward)
        suggestions_data.append({
            "id": ward['code'],
            "type": 'area',
            'sub_type': 'ward',
            "text": ward['name'],
            "sub_text": district['path'],
        })

    return suggestions_data