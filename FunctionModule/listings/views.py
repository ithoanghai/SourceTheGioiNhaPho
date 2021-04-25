from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from pydantic import BaseModel

from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing
from ..cadastral.constants import state_data, district_data


class ListingSearchQuery(BaseModel):
    keywords: str = None
    state: int = None
    bedrooms: int = None
    price: int = None


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/search.html', context)


def listing(request, listing_id):
    context = {
        'listing': get_object_or_404(Listing, pk=listing_id)
    }

    return render(request, 'listings/detail.html', context)

def detail(request):
    listing_id = request.GET.get('id', '')
    context = {
        'listing': get_object_or_404(Listing, pk=listing_id)
    }

    return render(request, 'listings/detail.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Trantype
    if 'trantype' in request.GET:
        trantype = request.GET['trantype']
        if trantype:
            queryset_list = queryset_list.filter(transaction_type=trantype)

    # Housetype
    if 'housetype' in request.GET:
        housetype = request.GET['housetype']
        if housetype:
            queryset_list = queryset_list.filter(transaction_type=housetype)

    # urban_area
    if 'urban_area' in request.GET:
        urban_area = request.GET['urban_area']
        if urban_area:
            queryset_list = queryset_list.filter(urban_area = housetype)

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query = Q(description__icontains=keywords) | Q(name__icontains=keywords)
            queryset_list = queryset_list.filter(query)

    # Address
            if 'address' in request.GET:
                address = request.GET['address']
                if address:
                    queryset_list = queryset_list.filter(address=address)

    # street
        if 'street' in request.GET:
            street = request.GET['street']
            if street:
                queryset_list = queryset_list.filter(address=street)

    # District
        if 'district' in request.GET:
            district = request.GET['district']
            if district:
                queryset_list = queryset_list.filter(district=district)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query = Q(price__lte=price) | Q(sale_price__lte=price)
            queryset_list = queryset_list.filter(query)


    context = {
        'listings': queryset_list,
        'state_data': state_data,
    }

    return render(request, 'listings/search.html', context)

def sell_with_us(request):
    context = {
    }

    return render(request, 'listings/sellWithUs.html', context)


def buy_with_us(request):
    context = {
    }

    return render(request, 'listings/buyWithUs.html', context)


def rent_with_us(request):
    context = {
    }

    return render(request, 'listings/rentWithUs.html', context)
