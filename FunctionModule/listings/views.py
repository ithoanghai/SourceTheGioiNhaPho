import os
import requests
import random
import string
import datetime

from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import upper
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_str
from django.views.generic import DetailView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from FunctionModule.hitcount.views import HitCountDetailView
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.rest_framework import DjangoFilterBackend
from pydantic import BaseModel
from rest_framework import status, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from FunctionModule.cadastral.lookups import get_all_states, get_all_districts, get_district
from FunctionModule.listings import get_short_title_from_house_type, get_short_title_from_transaction_type
from FunctionModule.hitcount.views import HitCountDetailView
from TownhouseWorldRealestate import settings
from TownhouseWorldRealestate.filters import ListingFilter

from . import HouseType
from .forms import ListingForm, ListingImageFormSet
from .models import ListingImage
from .search import get_suggestions, prepare_listing_queryset
from .serializers import *
from ..cadastral.constants import district_data


class ListingSearchQuery(BaseModel):
    keywords: str = None
    state: int = None
    bedrooms: int = None
    price: int = None


def index(request):
    listings = Listing.objects.order_by('priority', 'price', '-date_update').filter(is_published=True, is_advertising=False)

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
    listings_neighborhood = Listing.objects.order_by('priority', '-date_update').filter(is_published=True, is_advertising=False,
                                                                    state__icontains=listing_detail.state)
    if listing_detail.district:
        listings_neighborhood = listings_neighborhood.filter(Q(district__icontains=listing_detail.district))
    if listing_detail.ward:
        listings_neighborhood = listings_neighborhood.filter(Q(ward__icontains=listing_detail.ward))
    if listing_detail.street:
        listings_neighborhood = listings_neighborhood | listings_neighborhood.filter(Q(street__icontains=listing_detail.street))
    if listing_detail.urban_area:
        listings_neighborhood = listings_neighborhood | listings_neighborhood.filter(Q(urban_area__icontains=listing_detail.urban_area))
    listings_neighborhood = ((listings_neighborhood)[:10])
    listings_same = (Listing.objects.order_by('priority', '-date_update').filter(is_published=True, is_advertising=False,
                                          price__gt=listing_detail.price-1, price__lt=listing_detail.price+1 , house_type=listing_detail.house_type,
                                                                               area__gt=listing_detail.area-2, area__lt=listing_detail.area+2)[:30])
    context = {
        'listing': listing_detail,
        'environment': settings.ENVIRONMENT,
        'listings_neighborhood': listings_neighborhood,
        'listings_same': listings_same
    }

    return render(request, 'listings/listing_detail.html', context)


def search(request):
    if request.GET.get('trans'):
        transtype = get_short_title_from_transaction_type(request.GET.get('trans'))
    else:
        transtype=''
    if request.GET.get('hoty'):
        housetype = get_short_title_from_house_type(request.GET.get('hoty'))
    else:
        housetype=''
    if request.GET.get('adv'):
        advertising = "rao v???t "
    else:
        advertising=''
    if request.GET.get('keys'):
        keywords = request.GET.get('keys')
    else:
        keywords=''
    if request.GET.get('so'):
        sort = 'h??ng ?????u '
    else:
        sort=''
    context = {
        'listings': [],
        'state_data': get_all_states(),
        'districts': get_all_districts(),
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
        'environment': settings.ENVIRONMENT,
        "pagination": {},
        'sortOption': 'priority',
        'state': request.GET.get('state'),
        'district': request.GET.get('district'),
        'word': request.GET.get('keys'),
        'transtype': transtype,
        'housetype': housetype,
        'advertising': advertising,
        'keywords': keywords,
        'sort': sort,
    }

    return render(request, 'listings/search.html', context)


#class ListingCreateView(LoginRequiredMixin, CreateView):
class ListingCreateView(CreateView):
    model = Listing
    form_class = ListingForm
    success_url = reverse_lazy('mylistingpost')
    #success_url = None
    template_name = 'listings/listing_form.html'
    login_url = 'admin/'
    #redirect_field_name = "next"

    def get_initial(self):
        return {'user': self.request.user}

    def get_context_data(self, **kwargs):
        context = super(ListingCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['listing_image_formset'] = ListingImageFormSet(self.request.POST, **self.request.FILES)
        else:
            context['listing_image_formset'] = ListingImageFormSet()
        return context

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
            created = datetime.datetime.now()
            code = f'POST{created.strftime("%y%m")}'.join(random.choice(string.ascii_letters + string.digits) for i in range(2))
            self.object = form.save(commit=False)
            # any manual settings go here
            self.object.user = self.request.user
            self.object.code = upper(code)
            self.object.is_advertising = True
            self.object.is_published = False
            self.object.save()
            messages.success(self.request, 'B???n ???? g???i tin ????ng th??nh c??ng. Qu???n tr??? vi??n s??? ki???m duy???t tr?????c khi ????ng.')
            return super().form_valid(form)
        except Listing.DoesNotExist:
            messages.error(self.request,
                             'Tin ????ng c???a b???n b??? l???i. Xin h??y ????ng l???i ho???c li??n h??? hotline ????? ???????c h??? tr???.')

        return render(self.request, 'listings/postListingSuccess.html')


def load_districts(request):
    state = request.GET.get('state')
    if state is not None:
        districts = get_district(state)
    else:
        districts = get_all_districts()
    return render(request, 'listings/district_ddl_options.html', {'districts': districts})


def mylistingpost(request):
    if request.user.is_authenticated and request.method == 'GET':
        listings = Listing.objects.filter(user=request.user, is_advertising=True).order_by('-date_update')
        paginator = Paginator(listings, 10)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        context = {
            'listings': paged_listings,
        }

        return render(request, 'listings/myListingPosts.html', context)
    else:
        return render(request, 'accounts/_profile.html')


def mylisting(request):
    if request.user.is_authenticated and request.method == 'GET':
        listings = Listing.objects.filter(user=request.user, is_advertising=False).order_by('-date_update')
        paginator = Paginator(listings, 10)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        context = {
            'listings': paged_listings,
        }

        return render(request, 'listings/myListings.html', context)
    else:
        return render(request, 'accounts/_profile.html')


def sellleaseus(request):
    context = {
        'path': request.path,
    }

    return render(request, 'listings/sellLeaseWithUs.html', context)


def buywithus(request):
    context = {
        'path': request.path,
    }

    return render(request, 'listings/buyWithUs.html', context)


def rentwithus(request):
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
        return queryset.order_by('-date_update')

    def post(self, request, *args, **kwargs):
        id_pk = self.kwargs.get('id', None)
        url = reverse('listing-detail', kwargs={'id': id_pk})
        request.data.update({force_str('listing'): force_str(url)})

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
    # code t???o nh??n b???n l???ch s??? b???t ?????ng s???n t???i ????y
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
                return render(request, 'listings/listing_form.html.html', context)
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
                date_created = timezone.now()
                # #  Check if user has made inquiry already
                user_id = request.user.id
                has_listing = Listing.objects.filter(address=address, user_id=user_id,
                                                     date_created__gte=date_created)
                if has_listing:
                    messages.error(request,
                                   'B???n ???? g???i y??u c???u t???i ch??ng t??i v??? tin ????ng n??y. Xin th??? g???i l???i y??u c???u sau.')
                    render(request, 'listings/postListingSuccess.html', context)
                if area.isnumeric() and width.isnumeric() and floor.isnumeric() and price.isnumeric():
                    listing = Listing.objects.create(user_id=user_id, is_advertising=True, is_published=False,
                                                     transaction_type=trantypes, house_type=housetype, code=code,
                                                     title=title,
                                                     description=description, street=street, district=district,
                                                     address=address, area=area, width=width, floors=int(floor),
                                                     price=price)
                else:
                    messages.error(request, 'B???n nh???p sai d??? li???u.')
                    return HttpResponseRedirect(reverse('admin'))

                if request.FILES.get('photomain', None) is not None:
                    ListingImage.objects.create(listing_id=listing.id, photo=photomain)
                    messages.success(request, 'B???n ???? g???i tin ????ng th??nh c??ng. Qu???n tr??? vi??n s??? ki???m duy???t tr?????c khi ????ng.')
                    return render(request, 'listings/postListingSuccess.html', context)
        else:
            return HttpResponseRedirect(reverse('admin'))

    except ValidationError:
        messages.error(request, 'Th??ng tin b???n nh???p kh??ng ????ng.')
        return HttpResponseRedirect(reverse('postlistings'))