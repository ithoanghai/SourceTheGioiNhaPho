from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import force_text
from django_filters.rest_framework import DjangoFilterBackend
from pydantic import BaseModel
from rest_framework import status, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import ListingFilter
from .search import prepare_listing_queryset
from .serializers import *
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
    listing_detail = get_object_or_404(Listing, pk=listing_id)
    listings_neighborhood = Listing.objects.order_by('-list_date').filter(state=listing_detail.state).exclude(
        id=listing_id)[:10]
    listings_same = (Listing.objects
                         .filter(house_type=listing_detail.house_type, area=listing_detail.area)
                         .exclude(id=listing_id)
                         .order_by('-list_date')[:10])
    context = {
        'listing': listing_detail,
        'listings_neighborhood': listings_neighborhood,
        'listings_same': listings_same
    }

    return render(request, 'listings/detail.html', context)


def detail(request):
    listing_id = request.GET.get('id', '')
    listing_detail = get_object_or_404(Listing, pk=listing_id)
    listings_neighborhood = Listing.objects.order_by('-list_date').filter(state=listing_detail.state)[:10]
    context = {
        'listing': listing_detail,
        'listings_neighborhood': listings_neighborhood
    }

    return render(request, 'listings/detail.html', context)


def search(request):
    hn_district = district_data['01']
    queryset_list = prepare_listing_queryset(request.GET)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    limit = request.GET.get('limit', 10)
    offset = (page - 1) * limit
    paginator = Paginator(queryset_list, limit)
    total_pages = paginator.num_pages
    next_5_pages = page + 5 if page + 5 < total_pages else total_pages
    min_page = page - 1 if page - 1 > 0 else page

    try:
        listings = paginator.get_page(page)
    except Exception:
        listings = paginator.get_page(1)

    context = {
        'listings': listings,
        'state_data': state_data,
        'districts': hn_district,
        'environment': settings.ENVIRONMENT,
        "pagination": {
            'current_page': page,
            'next_5_pages': list(range(min_page, next_5_pages)),
            'limit': limit,
            'offset': offset,
            'total': queryset_list.count()
        }
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


@api_view(['GET', 'POST'])
def listing_api_view(request):
    """
    List all listings, or create a new listing.
    """
    if request.method == 'GET':
        listings = Listing.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = ListingSerializer(listings, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ListingFilter

    def get_queryset(self):
        id_pk = self.kwargs.get('id', None)
        # queryset = Listing.objects.filter(id=id_pk)
        queryset = Listing.objects.all()
        return queryset.order_by('list_date')

    def post(self, request, *args, **kwargs):
        id_pk = self.kwargs.get('id', None)
        url = reverse('listing-detail', kwargs={'id': id_pk})
        request.data.update({force_text('listing'): force_text(url)})

        return super(ListingsAPIView, self).post(request, *args, **kwargs)


class ListingAPIAllView(mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        serializer = ListingSerializer(self.queryset, many=True, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
