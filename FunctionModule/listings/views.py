from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import force_text
from django_filters.rest_framework import DjangoFilterBackend
from pydantic import BaseModel
from rest_framework import status, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import ListingFilter
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
    listings_neighborhood = Listing.objects.order_by('-list_date').filter(state=listing_detail.state)[:10]
    listings_same = Listing.objects.order_by('-list_date').filter(house_type=listing_detail.house_type,
                                                                  area=listing_detail.area)[:10]
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
    queryset_list = Listing.objects.order_by('-list_date')
    hn_district = district_data['01']

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
            queryset_list = queryset_list.filter(urban_area=urban_area)

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
            district_code = next(x['code'] for x in hn_district if x['slug'] == district)
            queryset_list = queryset_list.filter(district=district_code)

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

    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 20)
    offset = (page - 1) * limit

    context = {
        'listings': queryset_list[offset: limit + offset],
        'state_data': state_data,
        'districts': hn_district,
        'pagination': {
            'current_page': page,
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
