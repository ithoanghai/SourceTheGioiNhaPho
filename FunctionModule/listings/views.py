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

from FunctionModule.cadastral.lookups import get_default_districts, get_all_states
from .filters import ListingFilter
from .serializers import *


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
    listings_neighborhood = Listing.objects.order_by('-list_date').filter(is_published=True,
                                                                          state=listing_detail.state).exclude(
        id=listing_id)[:10]
    listings_same = (Listing.objects
                         .filter(is_published=True, house_type=listing_detail.house_type,
                                 area=listing_detail.area)
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
    listings_neighborhood = Listing.objects.order_by('-list_date').filter(is_published=True,
                                                                          state=listing_detail.state)[:10]
    context = {
        'listing': listing_detail,
        'environment': settings.ENVIRONMENT,
        'listings_neighborhood': listings_neighborhood
    }

    return render(request, 'listings/detail.html', context)


def search(request):
    context = {
        'listings': [],
        'state_data': get_all_states(),
        'districts': get_default_districts(),
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
        'environment': settings.ENVIRONMENT,
        "pagination": {}
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
