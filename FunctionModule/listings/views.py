import random
import string

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from hitcount.views import HitCountDetailView
from django.views.decorators.csrf import ensure_csrf_cookie
from pydantic import BaseModel
from rest_framework import status, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from FunctionModule.cadastral.lookups import get_all_states, get_all_districts

from . import HouseType
from .filters import ListingFilter
from .models import ListingImage
from .serializers import *
from ..cadastral.constants import district_data


class ListingSearchQuery(BaseModel):
    keywords: str = None
    state: int = None
    bedrooms: int = None
    price: int = None


def index(request):
    listings = Listing.objects.order_by('priority', 'price', '-list_date').filter(is_published=True, is_advertising=False)

    paginator = Paginator(listings, 100)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
        'sortOption': 'priority'
    }

    return render(request, 'listings/search.html', context)


def listing(request, listing_id):
    ListingDetailJSONView()
    listing_detail = get_object_or_404(Listing, pk=listing_id)
    listings_neighborhood = (
    Listing.objects.order_by('priority', '-list_date').filter(is_published=True, is_advertising=False,
                                                              state=listing_detail.state)[:10])
    listings_same = (Listing.objects.order_by('priority', '-list_date').filter(is_published=True, is_advertising=False,
                                                                               house_type=listing_detail.house_type,
                                                                               area=listing_detail.area)[:30])

    context = {
        'listing': listing_detail,
        'environment': settings.ENVIRONMENT,
        'listings_neighborhood': listings_neighborhood,
        'listings_same': listings_same
    }

    return render(request, 'listings/listing_detail.html', context)


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
    try:
        houseTypes = HouseType.choices
        state_code = "01"
        hanoi_district_list = district_data[state_code]
        district_choices = {}
        alphabet = string.ascii_letters + string.digits
        code = f'POST'.join(random.choice(alphabet) for i in range(2))
        for item in district_choices:  # type: dict
            district_choices[item['name']] = item['code']
        context = {
            'houseTypes': houseTypes,
            'district_choices': district_choices
        }
        if request.user.is_authenticated:
            if request.method == 'GET':
                return render(request, 'listings/postListing.html', context)
            elif request.method == 'POST':
                trantypes = request.POST['trantypes']
                housetype = request.POST['housetype']
                title = request.POST['title']
                description = request.POST['description']
                street = request.POST['street']
                address = request.POST['address']
                district = '008'
                area = request.POST['area']
                width = request.POST['width']
                floor = request.POST['floor']
                price = request.POST['price']
                if request.FILES.get('photomain', None) is not None:
                    photomain = request.FILES.get('photomain')
                else:
                    photomain = request.POST['photomain']
                list_date = timezone.now()
                # #  Check if user has made inquiry already
                user_id = request.user.id
                has_listing = Listing.objects.filter(address=address, user_id=user_id,
                                                     list_date__gte=list_date)
                if has_listing:
                    messages.error(request,
                                   'Bạn đã gửi yêu cầu tới chúng tôi về tin đăng này. Xin thử gửi lại yêu cầu sau.')
                    return redirect('post_listings')
                if area.isnumeric() and width.isnumeric() and floor.isnumeric() and price.isnumeric():
                    listing = Listing.objects.create(user_id=user_id, is_advertising=True, is_published=False,
                                                     transaction_type=trantypes, house_type=housetype, code=code,
                                                     title=title,
                                                     description=description, street=street, district=district,
                                                     address=address, area=area, width=width, floors=int(floor),
                                                     price=price)
                else:
                    messages.error(request, 'Bạn nhập sai dữ liệu.')
                    return redirect('post_listings')

                if request.FILES.get('photomain', None) is not None:
                    ListingImage.objects.create(listing_id=listing.id, photo=photomain)
                    messages.success(request, 'Bạn đã gửi tin đăng thành công. Quản trị viên sẽ kiểm duyệt trước khi đăng.')
                    return render(request, 'listings/postListingSuccess.html', context)
        else:
            return redirect('login')

    except ValidationError:
        messages.error(request, 'Thông tin bạn nhập không đúng.')
        return redirect('post_listings')


def my_listing_post(request):
    if request.user.is_authenticated and request.method == 'GET':
        listings = Listing.objects.filter(user=request.user, is_advertising=True).order_by('-list_date')
        paginator = Paginator(listings, 10)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        context = {
            'listings': paged_listings,
        }

        return render(request, 'listings/myListingPosts.html', context)
    else:
        return render(request, 'accounts/_profile.html')


def my_listing(request):
    if request.user.is_authenticated and request.method == 'GET':
        listings = Listing.objects.filter(user=request.user, is_advertising=False).order_by('-list_date')
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
        'path': request.path,
    }

    return render(request, 'listings/sellLeaseWithUs.html', context)


def buy_with_us(request):
    context = {
        'path': request.path,
    }

    return render(request, 'listings/buyWithUs.html', context)


def rent_with_us(request):
    context = {
        'path': request.path,
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


class ListingMixinDetailView(object):
    """
    Mixin to save us some typing.  Adds context for us!
    """
    model = Listing

    def get_context_data(self, **kwargs):
        context = super(ListingMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Listing.objects.all()[:5]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context


class ListingDetailJSONView(ListingMixinDetailView, DetailView):
    template_name = 'listings/listing_detail.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ListingDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)


class ListingCountHitDetailView(ListingMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True


class ListingDetailView(ListingMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    pass


def listinghistoryadd(request, extra_context=None):
    # code tạo nhân bản lịch sử bất động sản tại đây
    try:
        houseTypes = HouseType.choices
        state_code = "01"
        hanoi_district_list = district_data[state_code]
        district_choices = {}
        alphabet = string.ascii_letters + string.digits
        code = f'POST'.join(random.choice(alphabet) for i in range(2))
        for item in district_choices:  # type: dict
            district_choices[item['name']] = item['code']
        context = {
            'houseTypes': houseTypes,
            'district_choices': district_choices
        }
        if request.user.is_authenticated:
            if request.method == 'GET':
                return render(request, 'listings/postListing.html', context)
            elif request.method == 'POST':
                trantypes = request.POST['trantypes']
                housetype = request.POST['housetype']
                title = request.POST['title']
                description = request.POST['description']
                street = request.POST['street']
                address = request.POST['address']
                district = '008'
                area = request.POST['area']
                width = request.POST['width']
                floor = request.POST['floor']
                price = request.POST['price']
                if request.FILES.get('photomain', None) is not None:
                    photomain = request.FILES.get('photomain')
                else:
                    photomain = request.POST['photomain']
                list_date = timezone.now()
                # #  Check if user has made inquiry already
                user_id = request.user.id
                has_listing = Listing.objects.filter(address=address, user_id=user_id,
                                                     list_date__gte=list_date)
                if has_listing:
                    messages.error(request,
                                   'Bạn đã gửi yêu cầu tới chúng tôi về tin đăng này. Xin thử gửi lại yêu cầu sau.')
                    return redirect('post_listings')
                if area.isnumeric() and width.isnumeric() and floor.isnumeric() and price.isnumeric():
                    listing = Listing.objects.create(user_id=user_id, is_advertising=True, is_published=False,
                                                     transaction_type=trantypes, house_type=housetype, code=code,
                                                     title=title,
                                                     description=description, street=street, district=district,
                                                     address=address, area=area, width=width, floors=int(floor),
                                                     price=price)
                else:
                    messages.error(request, 'Bạn nhập sai dữ liệu.')
                    return redirect('post_listings')

                if request.FILES.get('photomain', None) is not None:
                    ListingImage.objects.create(listing_id=listing.id, photo=photomain)
                    messages.success(request, 'Bạn đã gửi tin đăng thành công. Quản trị viên sẽ kiểm duyệt trước khi đăng.')
                    return render(request, 'listings/postListingSuccess.html', context)
        else:
            return redirect('login')

    except ValidationError:
        messages.error(request, 'Thông tin bạn nhập không đúng.')
        return redirect('post_listings')