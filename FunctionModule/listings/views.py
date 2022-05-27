from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django_filters.rest_framework import DjangoFilterBackend
from pydantic import BaseModel
from rest_framework import status, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from FunctionModule.cadastral.lookups import get_all_states, get_all_districts
from . import Status, TransactionType
from .filters import ListingFilter
from .serializers import *


class ListingSearchQuery(BaseModel):
    keywords: str = None
    state: int = None
    bedrooms: int = None
    price: int = None


def index(request):
    listings = Listing.objects.order_by('-priority','-list_date').filter(is_published=True, is_advertising=False)

    paginator = Paginator(listings, 100)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
        'sortOption': 'priority'
    }

    return render(request, 'listings/search.html', context)


def listing(request, listing_id):
    listing_detail = get_object_or_404(Listing, pk=listing_id)
    listings_neighborhood = (Listing.objects.order_by('-priority','-list_date').filter(is_published=True, is_advertising=False,
                                                                          state=listing_detail.state)[:10])
    listings_same = (Listing.objects.order_by('-priority','-list_date').filter(is_published=True, is_advertising=False, house_type=listing_detail.house_type,area=listing_detail.area)[:30])

    context = {
        'listing': listing_detail,
        'environment': settings.ENVIRONMENT,
        'listings_neighborhood': listings_neighborhood,
        'listings_same': listings_same
    }

    return render(request, 'listings/detail.html', context)


def search(request):
    context = {
        'listings': [],
        'state_data': get_all_states(),
        'districts': get_all_districts(),
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
        'environment': settings.ENVIRONMENT,
        "pagination": {},
        'sortOption': 'priority',
    }

    return render(request, 'listings/search.html', context)


def post_listing(request):
    context = {
    }
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'listings/postListing.html', context)
        elif request.method == 'POST':
            # listing_id = request.POST['listing_id']
            # lastname = request.POST['lastname']
            # firstname = request.POST['firstname']
            # name = f'{firstname} {lastname}'
            # email = request.POST['email']
            # phone = request.POST['phone']
            # message = request.POST['message']
            # user_id = request.POST.get('user_id', None)
            # yesterday = timezone.now() - timedelta(days=1)
            # #  Check if user has made inquiry already
            # if request.user.is_authenticated:
            #     user_id = request.user.id
            #     has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id,
            #                                            contact_date__gte=yesterday)
            #     if has_contacted:
            #         messages.error(request,
            #                        'Bạn đã gửi yêu cầu tới chúng tôi về căn hộ này. Xin thử gửi lại yêu cầu sau.')
            #         return redirect('/listings/' + listing_id)
            # else:
            #     ses_id = request.session.session_key
            #     print(ses_id)
            #
            # listing = Listing.objects.get(pk=listing_id)

            # Contact.objects.create(listing=listing.code, listing_id=listing_id, name=name, email=email,
            #                        phone=phone, message=message, user_id=user_id)
            #
            # messages.success(request, 'Yêu cầu được gửi thành công. Chúng tôi sẽ liên lạc lại với bạn sớm nhất.')

            return render(request, 'listings/postListingSuccess.html', context)
    else:
        return redirect('login')


def post_listings(request,typeTran):
    listings = Listing.objects.order_by('-priority','-list_date').filter(is_published=True, is_advertising=True, transaction_type=typeTran,)

    paginator = Paginator(listings, 100)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/postListing.html', context)


def my_listing(request):
    if request.user.is_authenticated and request.method == 'GET':
        listings = Listing.objects.filter(user=request.user).order_by('-list_date')
        paginator = Paginator(listings, 10)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        context = {
            'listings': paged_listings,
        }

        return render(request, 'listings/myListings.html', context)
    else:
        return render(request, 'accounts/_profile.html')


def sell_lease_with_us(request):
    context = {
    }

    return render(request, 'listings/sellLeaseWithUs.html', context)


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
