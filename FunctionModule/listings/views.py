from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from pydantic import BaseModel

from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing
from ..cadastral.constants import state_data


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

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    context = {
        'listing': get_object_or_404(Listing, pk=listing_id)
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query = Q(description__icontains=keywords) | Q(name__icontains=keywords)
            queryset_list = queryset_list.filter(query)

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
        'state_data': state_data,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)
