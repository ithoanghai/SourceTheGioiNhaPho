import io
import warnings
import json
import csv
import pytz
import os
import tempfile
from datetime import date, datetime
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.text import slugify
from geopy.geocoders import Nominatim
from string import digits
from decimal import Decimal
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django import forms
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from TownhouseWorldRealestate.filters import ChoicesFieldListFilter, DateFieldListFilter, BooleanFieldListFilter
from .forms import ListingAdminForm, ImportListingForm, ImageForm, ImageFormSet, ContractImageForm, \
    ContractImageFormSet, ImportForm, ExportForm
from .models import Listing, ListingImage, ListingVideo, ContractImage, ListingHistory
from .choices import district_default_choices, Exhaustive
from .choices import Status, RoadType, Condition, HouseType, FurnishType, RegistrationType
from ..transactions.models import Transaction
from import_export import resources
from import_export.admin import ImportExportModelAdmin, logger
from import_export.forms import ImportExportFormBase
from import_export.signals import post_export
from FunctionModule.accounts.models import User
from FunctionModule.cadastral.constants import district_data
from FunctionModule.cadastral.lookups import get_district_name
from FunctionModule.listings.helpers import print_trace, get_house_type_short, get_short_title_from_house_type
from FunctionModule.listings.models import Listing, Status, TransactionType, HouseType, RoadType, ListingHistory
from FunctionModule.realtors.choices import Position, Workplace, Title
from FunctionModule.realtors.models import Realtor


def read_header(header_row, data_type):
    if data_type == 'K1':
        logger.info(f"data_type {data_type} Nha Pho VN")
        header_dict = {
            "tieude": 0,
            "mota": 1,
            "motadauchu": 2,
            "anh-nha": 3,
            "anh-so": 4,
            "tgian": 5,
            "hien-trang": 6,
            "dia-chi": 7,
            "pho": 8,
            "quan": 9,
            "thong-so": 10,
            "gia": 11,
            "dau-chu": 12,
            "sdt": 13,
            "don-vi": 14,
            "dac-diem": 15,
            "huong": 16,
            "dt": 20,
            "trm2": 21,
            "hientrang": 22,
            # "thanh-pho": 20,
            # "so-tang": 23,
            # "mat-tien": 23,
            # "hoa-hong": 23,
            # "nguon": 23,
        }
    elif data_type == 'K2':
        logger.info(f"data_type {data_type} Thien Khoi")
        header_dict = {
            "tieude": 0,
            "mota": 1,
            "motadauchu": 2,
            "anh-nha": 3,
            "anh-so": 4,
            "dia-chi": 5,
            "dt": 6,
            "so-tang": 7,
            "mat-tien": 8,
            "gia": 9,
            "quan": 10,
            "dau-chu": 11,
            "sdt": 12,
            "hoa-hong": 13,
            "nguon": 14,
            "hien-trang": 15,
            "tgian": 16,
            "thanh-pho": 18,
            "don-vi": 19,
            "pho": 20,
            "dac-diem": 21,
            "huong": 22,
        }

    for index, field in enumerate(header_row):
        field = field.replace('??', 'd')
        field = slugify(field)
        if field in header_dict:
            if field == 'pho' and index > 3:
                continue
            header_dict[field] = index
    return header_dict


def prepare_fb_headers():
    return [
        "home_listing_id",  # B???t bu???c
        "name",  # B???t bu???c
        "description",
        "availability",  # B???t bu???c
        "price",                     #B???t bu???c | The cost and currency of the home listing. The price is a number followed by the currency code (ISO 4217 standards)
        "url",  # B???t bu???c | The URL of the specific page where people can view the listing.
        "address.addr1",  # B???t bu???c
        "address.city",  # B???t bu???c
        "address.country",  # B???t bu???c
        "latitude",  # B???t bu???c
        "longitude",  # B???t bu???c
        "neighborhood[0]",  # B???t bu???c
        "image[0].url",  # B???t bu???c
        "image[0].tag[0]",  # B???t bu???c

        "home_listing_group_id",
        "custom_number_0",
        "ac_type",
        "agent_name",
        "agent_company",
        "furnish_type",
        "tenure_type",
        "sale_type",
        "garden_type",
        "days_on_market",
        "fee_schedule_url",
        "heating_type",
        "laundry_type",
        "listing_type",
        "agent_rera_id",
        "property_rera_id",
        "num_baths",
        "num_beds",
        "num_rooms",
        "num_units",
        "parking_type",
        "partner_verification",
        "pet_policy",
        "min_price",
        "max_price",
        "property_type",
        "area_size",
        "built_up_area_size",
        "property_tax",
        "condo_fee",
        "coownership_charge",
        "parking_spaces",
        "area_unit",
        "year_built",
        "address.addr2",
        "address.addr3",
        "address.city_id",
        "address.region",
        "address.postal_code",
        "address.unit_number",
        "energy_rating_eu.grade",
        "energy_rating_eu.value",
        "co2_emission_rating_eu.grade",
        "co2_emission_rating_eu.value",
        "additional_fees_description",
        "num_pets_allowed",
        "land_area_size",
        "security_deposit",
        "holding_deposit",
        "application_fee",
        "pet_deposit",
        "pet_monthly_fee",
        "floor_types[0]",
        "unit_features[0]",
        "construction_status",
        "coownership_num_lots",
        "coownership_status",
        "coownership_proceedings_status",
        "special_offers[0]",
        "pet_restrictions[0]",
        "building_amenities[0]",
        "broker_fee",
        "first_month_rent",
        "last_month_rent",
        "utilities_included_in_rent[0]",
        "rental_room_type",
        "private_room_bathroom_type",
        "number_of_co_renters",
        "private_room_area_size",
        "virtual_tour_url",

        "visibility",
        "condition",
        "image_link",
        "additional_image_link",
    ]


def get_main_photo_url(listing):
    main_photo_url = listing.main_photo
    if main_photo_url is None:
        photo_url = f'https://thegioinhaphovietnam.com.vn/static/img/default_house_type/{listing.house_type}.jpg'
    else:
        photo_url = main_photo_url.url
    return photo_url


def get_description(listing):
    description = f'<div><p><bold> M?? B??S: %s </bold></p> </div> ' \
                  f'<p> %s </p> <br>' \
                  % (listing.code, listing.description)
    if listing.furniture_design is not None:
        description = description + '<br> <p> %s </p>' + listing.furniture_design
    if listing.living_facilities is not None:
        description = description + '<br> <p> %s </p>' + listing.living_facilities
    if listing.location_advantage is not None:
        description = description + '<br> <p> %s </p>' + listing.location_advantage
    if listing.residential_community is not None:
        description = description + '<br> <p> %s </p>' + listing.residential_community
    if listing.regional_welfare is not None:
        description = description + '<br> <p> %s </p>' + listing.regional_welfare
    if listing.salient_features is not None:
        description = description + '<br> <p> %s </p>' + listing.salient_features
    if get_video_link(listing) != "":
        description = description + '<p> ????? xem video B??S n??y, b???n truy c???p Link Video Youtube sau %s </p> </br>' % (get_video_link(listing))
    description1 = f'<p>Li??n h??? ngay Th??? gi???i Nh?? Ph??? ????? ???????c t?? v???n, xem b??s</p>' \
                  f'<p>------------o0o--------------</p>' \
                  f'<p>B???T ?????NG S???N TH??? GI???I NH?? PH???</p>' \
                  f'<p>- H??ng ch???c ngh??n s???n ph???m B??S, cam k???t th??ng tin th???t, ch??nh x??c 100%, kh??ng c?? th??ng tin ???o</p>' \
                  f'<p>- T??m ki???m B??S d??? d??ng t???i website c???a TGNP: https://Thegioinhaphovietnam.com.vn</p>' \
                  f'<p>- Hotline: 0916.286.256 - 0971.841.941 - 09.6439.9436 (Call/Zalo/Facebook)</p>' \
                  f'<p>- <a href= "https://www.facebook.com/TheGioiNhaPhoVietNam">C???a h??ng Facebook.com/TheGioiNhaPhoVietNam</a> </p>' \
                  f'<p>- <a href= "https://www.facebook.com/groups/khohang.thegioinhaphovietnam">Kho h??ng Facebook.com/groups/khohang.thegioinhaphovietnam</a> </p>' \
                  f'<p>- <a href= "https://www.youtube.com/channel/UCiW13E8_8AHnHGiJGeZliug">K??nh Youtube KHO H??NG TH??? GI???I NH?? PH???</a> </p>'
    return description + description1


def get_parking_type(road_type):
    if road_type == RoadType.ALLEY_CAR_2:
        return 'off_street'
    elif road_type == RoadType.ALLEY_CAR_TRIBIKE:
        return 'street'
    else:
        return 'none'


def get_availability(listing):
    if listing.status == Status.SELLING:
        return 'available_soon'
    elif listing.status == Status.SALE:
        return 'off_market'
    elif listing.status == Status.STOP_SELLING:
        return 'sale_pending'
    elif listing.status == Status.SOLD:
        return 'recently_sold'


def get_visibility(listing):
    if listing.is_published == True:
        return 'published'
    else:
        return 'hidden'

 # return value  new, refurbished, used
def get_condition(listing):
    if listing.condition == Condition.NEW:
        return 'new'
    elif listing.condition == Condition.OLD:
        return 'used'
    else:
        return'refurbished'


def get_status(status):
    if status == Status.SELLING:
        return 'for_sale'
    elif status == Status.SALE:
        return 'for_sale'
    elif status == Status.SOLD:
        return 'recently_sold'
    else:
        return 'off_market'


def get_listing_type(listing):
    if listing.condition == Condition.NEW:
        return 'new_construction'
    else:
        return 'for_sale_by_owner'


 # return value  "new", "resale", "former"
def get_sale_type(listing):
    if listing.status == Status.SELLING:
        return 'new'
    elif listing.status == Status.SALE:
        return 'resale'
    else:
        return'former'


def get_property_type(listing):
    if listing.house_type == HouseType.STREET_HOUSE or listing.house_type == HouseType.LOFT_HOUSE or listing.house_type == HouseType.SHOP_HOUSE:
        return 'house'
    elif listing.house_type == HouseType.TOWN_HOUSE:
        return 'townhouse'
    elif listing.house_type == HouseType.APARTMENT or listing.house_type == HouseType.SERVICE_APARTMENT or listing.house_type == HouseType.OFFICE_TEL or listing.house_type == HouseType.OFFICE:
        return 'apartment'
    elif listing.status == HouseType.PENT_HOUSE:
        return 'penthouse'
    elif listing.house_type == HouseType.CONDO_TEL or listing.house_type == HouseType.BUILDING or listing.house_type == HouseType.BUILDING_BUSINESS:
        return 'condo'
    elif listing.house_type == HouseType.VILLA or listing.house_type == HouseType.VILLA_REST:
        return 'house_in_villa'
    elif listing.house_type == HouseType.LAND or listing.house_type == HouseType.LAND_BUSINESS or listing.house_type == HouseType.PLOT or listing.house_type == HouseType.PLOT or listing.house_type == HouseType.INDUSTRIAL_LAND:
        return 'land'
    elif listing.house_type == HouseType.WAREHOUSE_WORKSHOP:
        return 'manufactured'
    else:
        return'other'


    #"furnished", "semi-furnished", "unfurnished"
def get_furnish_type(listing):
    if listing.furnish_type == FurnishType.FURNISHED:
        return 'furnished'
    elif listing.furnish_type == FurnishType.SEMI_FURNISHED:
        return 'semi-furnished'
    else:
        return 'unfurnished'


    # "freehold", "leasehold", "strata_title", "cooperative", "power_of_attorney", "other",
    # "indonesia_hak_guna_banguan", "indonesia_hak_pakai", "indonesia_girik"
def get_tenure_type(listing):
        if listing.registration_type == RegistrationType.RED_PINK_BOOK or RegistrationType.VALID_DOCUMENTS:
            return 'strata_title'
        elif listing.registration_type == RegistrationType.BUSINESS_LICENSE or RegistrationType.CONSTRUCTION_LICENSE:
            return 'leasehold'
        elif listing.registration_type == RegistrationType.DONT_BOOK:
            return 'cooperative'
        else:
            return 'other'


# C??c gi?? tr??? ???????c c??ng nh???n cho nh???ng tr?????ng th??ng tin n??y bao g???m "garage", "none", "off_street", "other", "street"
def get_parking_type(listing):
    if listing.parking_type == RoadType.ALLEY_CAR_2 or listing.road_type == RoadType.ALLEY_CAR:
        return '1'
    else:
        return '0'


def get_parking_spaces(listing):
    if listing.road_type == RoadType.ALLEY_CAR_2 or listing.road_type == RoadType.ALLEY_CAR:
        return '1'
    else:
        return '0'


def get_additional_image_link_data(photos):
    list = ""
    for index, photo in enumerate(photos):
        list = list.__add__(f'https://thegioinhaphovietnam.com.vn{photo.url},')
    return list


def get_video_link(listing):
    link_main = ""
    for video in listing.videos:
        link_main = link_main.__add__(f'<a href="{video.video}">{video.video}</a>,')
    return link_main


def prepare_fb_listing_data(listing):
    price = listing.sale_price or listing.price
    url = reverse('listing_detail', kwargs={'listing_id': listing.id})
    full_url = f'https://thegioinhaphovietnam.com.vn{url}'
    main_photo_url = get_main_photo_url(listing)
    real_size = listing.area_real or listing.area
    listing_data = {
        "home_listing_id": listing.code, # B???t bu???c
        "name": f'{listing.code}', # B???t bu???c
        "description": get_description(listing), # B???t bu???c
        "availability": get_availability(listing), # B???t bu???c
        "price": f'{price:5.2f} VND', # B???t bu???c
        "url": full_url, # B???t bu???c | The URL of the specific page where people can view the listing.
        "address.addr1": f'%s, %s' % (listing.district_name(), listing.state_name()), # B???t bu???c
        "address.city": f'%s' % (listing.state), # B???t bu???c
        "address.country": f'Vi???t Nam', # B???t bu???c
        "latitude": listing.lat, # B???t bu???c
        "longitude": listing.long, # B???t bu???c
        "neighborhood[0]": listing.residential_community,  # B???t bu???c
        "image[0].url": main_photo_url,  # B???t bu???c
        "image[0].tag[0]": main_photo_url,  # B???t bu???c

        "home_listing_group_id": None,
        "custom_number_0":  1,
        "ac_type": "central",
        "agent_name": "Ho??ng H???i",
        "agent_company": "TGNP",
        "furnish_type": get_furnish_type(listing),
        "tenure_type": get_tenure_type(listing),
        "sale_type": get_sale_type(listing),
        "garden_type": None,
        "days_on_market": None,
        "fee_schedule_url": None,
        "heating_type": "central",
        "laundry_type": None,
        "listing_type": get_listing_type(listing),
        "agent_rera_id": None,
        "property_rera_id": None,
        "num_baths": listing.bathrooms if listing.bathrooms else None,
        "num_beds": listing.bedrooms,
        "num_rooms": None,
        "num_units": None,
        "parking_type": listing.parking_type,
        "partner_verification": "verified" if listing.is_verified else 'none',
        "pet_policy": None,
        "min_price": None,
        "max_price": None,
        "property_type": get_property_type(listing),
        "area_size": int(listing.area),
        "built_up_area_size": int(real_size),
        "property_tax": None,
        "condo_fee": None,
        "coownership_charge": None,
        "parking_spaces": None,
        "area_unit": None,  # Total area of unit; including outer walls; balcony.
        "year_built": "2022",
        "address.addr2": listing.ward_name(),
        "address.addr3": listing.street,
        "address.city_id": None,
        "address.region": listing.state,
        "address.postal_code": None,
        "address.unit_number": None,
        "energy_rating_eu.grade": None,
        "energy_rating_eu.value": None,
        "co2_emission_rating_eu.grade": None,
        "co2_emission_rating_eu.value": None,
        "additional_fees_description": None,
        "num_pets_allowed": None,
        "land_area_size": int(listing.area),
        "security_deposit": None,
        "holding_deposit": None,
        "application_fee": None,
        "pet_deposit": None,
        "pet_monthly_fee": None,
        "floor_types[0]": None,
        "unit_features[0]": None,
        "construction_status": None,
        "coownership_num_lots": None,
        "coownership_status": None,
        "coownership_proceedings_status": None,
        "special_offers[0]": None,
        "pet_restrictions[0]": None,
        "building_amenities[0]": None,
        "broker_fee": None,
        "first_month_rent": None,
        "last_month_rent": None,
        "utilities_included_in_rent[0]": None,
        "rental_room_type": None,
        "private_room_bathroom_type": None,
        "number_of_co_renters": None,
        "private_room_area_size": None,
        "virtual_tour_url": None,

        "visibility": get_visibility(listing),
        "condition": get_condition(listing),
        "additional_image_link": get_additional_image_link_data(listing.photos),
    }
    return listing_data


class ListingResource(resources.ModelResource):

    class Meta:
        model = Listing


class ListingPhotoAdmin(admin.TabularInline):
    model = ListingImage
    verbose_name = "H??NH ???NH CH???P B??S"
    form = ImageForm
    formset = ImageFormSet

    max_num = 25
    extra = 0


class ContractPhotoAdmin(admin.TabularInline):
    model = ContractImage
    verbose_name = "???NH H???P ?????NG TR??CH TH?????NG & PHI???U KH???O S??T B??S"
    form = ContractImageForm
    formset = ContractImageFormSet

    max_num = 10
    extra = 0


class ListingVideoAdmin(admin.TabularInline):
    model = ListingVideo
    extra = 0
    verbose_name = "VIDEO QUAY B??S"


class ListingHistoryInline(admin.TabularInline):
    model = ListingHistory
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created', 'area','floors', 'price', 'extra_data', 'warehouse', )


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'status', 'trantype', 'request_price', 'customer', 'realtor',)
    can_delete = False
    readonly_fields = ('date', 'realtor', 'customer',)


class ListingAdmin(ImportExportModelAdmin):
    resource_classes = [ListingResource]
    import_form_class = ImportForm
    export_form_class = ExportForm
    fieldsets = (
        ('TH??NG TIN CHUY??N VI??N', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('TH??NG TIN GIAO D???CH', {'fields': (
            ('transaction_type', 'house_type', 'is_exclusive', 'is_verified', ),)}),
        ('TH??NG TIN B???T ?????NG S???N', {'fields': (
            ('title', 'code'), ('description', 'extra_data'),
            ('area', 'floors', 'width'), ('price', 'registration_type', 'road_type'),
        )}),
        ('TR???NG TH??I KH???O S??T', {'fields': (
            ('exhaustive', 'liquidity_classification'), ('expert_comments',))}),
        ('?????A CH??? & V??? TR?? B??S', {'fields': (
            ('state', 'district', 'ward'), ('street', 'address', 'location'))}),
        ('TR???NG TH??I ????NG TIN', {
            'fields': (('date_created', 'date_update'), ('status', 'is_published', 'priority'),)}),
    )

    list_display = ('status', 'address', 'area', 'floors', 'width', 'price', 'average_price', 'road_type', 'house_type', 'district','created_date', 'is_advertising', 'is_published')
    list_display_links = ('address','price',)
    list_filter = (
        ('transaction_type', ChoicesFieldListFilter),
        ('status', ChoicesFieldListFilter),
        ('house_type', ChoicesFieldListFilter),
        ('road_type', ChoicesFieldListFilter),
        ('date_created', DateFieldListFilter),
        ('date_update', DateFieldListFilter),
        ('is_published', BooleanFieldListFilter),
        ('is_advertising', BooleanFieldListFilter),
        ('registration_type', ChoicesFieldListFilter),
        ('exhaustive', ChoicesFieldListFilter),
        ('liquidity_classification', ChoicesFieldListFilter),
        #('area', RangeNumericFilter),
        # ('floors', RangeNumericFilter),
        # ('width', RangeNumericFilter),
        # ('price', RangeNumericFilter),
        # ('average_price', RangeNumericFilter),
        # ('bedrooms', RangeNumericFilter),
        # ('priority', RangeNumericFilter),
    )
    #advanced_filter_fields = ('status', ('house_type', 'road_type'))
    list_editable = ()
    search_fields = ('id', 'title', 'code', 'address', 'area', 'price', 'house_type', 'road_type', 'urban_area',
                     'street', 'ward', 'district', 'state', 'date_created', 'date_update', 'extra_data')
    list_per_page = 100
    inlines = [ListingPhotoAdmin, ContractPhotoAdmin, ListingVideoAdmin, ListingHistoryInline, TransactionInline]

    actions = ['make_published', 'unpublished', 'sold', 'exhaustive']
    form = ListingAdminForm
    ordering = ('-date_update',)
    autocomplete_fields = ['user','realtor']
    sortable_by = ('address', 'area', 'floors', 'width', 'price', 'average_price', 'road_type', 'house_type', 'district','created_date')
    #delete_selected.short_description = 'X??a b???t ?????ng s???n ???? ch???n trong %(verbose_name_plural)'

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/listing.js', 'admin/js/filepond-4.28.2.min.js',
              'admin/js/micromodal-0.4.6.min.js', 'admin/js/admin-numeric-filter.js',
              'admin/js/nouislider.min.js','admin/js/wNumb.min.js')
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css', 'admin/css/filepond.min.css',
                    'admin/css/admin-numeric-filter.css', 'admin/css/nouislider.min.css')
        }

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(ListingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        realtor_list = Realtor.objects.filter(user=request.user)
        if realtor_list is not None:
            form.base_fields['realtor'].initial = realtor_list.first()
        form.base_fields['district'].choices = district_default_choices
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user',
            'realtor',
        }
        excludes = ('reward_person_mobile', 'extra_data')
        if request.user.is_superuser:
            form.base_fields['user'].disabled = True
        elif request.user.is_staff:
            for exc in excludes:
                if exc in form.base_fields:
                    form.base_fields[exc].widget = forms.HiddenInput()
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        else:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        return form

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: int = None,
        form_url: str = '',
        extra_context: dict = None
    ) -> HttpResponse:

        extra_context = extra_context or {}
        extra_context.update({
            'show_save_as_copy': True,
            'show_save_and_add_history': True,
            'transaction_history': True,
        })
        return super().changeform_view(request, object_id, extra_context=extra_context)

    def changelist_view(
        self,
        request: HttpRequest,
        form_url: str = '',
        extra_context: dict = None
    ) -> HttpResponse:

        extra_context = extra_context or {}
        extra_context.update({
            'extrabutton': True,
        })
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.is_staff:
            queryset = super().get_queryset(request)
            return queryset
        else:
            queryset_list = Listing.objects.order_by('-date_update')
            query = Q(realtor__user=request.user.id)
            query = query | Q(user=request.user)
            queryset_list = queryset_list.filter(query)
            return queryset_list

    # def get_exclude(self, request, obj=None):
    #     excluded = super().get_exclude(request, obj)
    #     user = request.user
    #     to_exclude = []
    #     if obj is None:
    #         to_exclude += []
    #     else:
    #         if not user.is_superuser:
    #             to_exclude.append('realtor')
    #             #if obj.realtor.user != user.id:
    #             #    to_exclude.append('address')
    #     try:
    #         return list(excluded) + to_exclude
    #     except TypeError:
    #         return to_exclude

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Chuy???n sang ch??? ????? ????ng c??ng khai cho {updated} b???t ?????ng s???n')

    def unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'???? ?????i tr???ng th??i ri??ng t?? cho {updated} b???t ?????ng s???n')

    def sold(self, request, queryset):
        updated = queryset.update(status=Status.SOLD)
        self.message_user(request, f'???? ?????i tr???ng th??i ???? b??n cho {updated} b???t ?????ng s???n')

    def exhaustive(self, request, queryset):
        updated = queryset.update(exhaustive=Exhaustive.PREPARE)
        self.message_user(request, f'???? l??n l???ch kh???o s??t {updated} b???t ?????ng s???n')

    make_published.short_description = _("????ng c??ng khai")
    unpublished.short_description = _("H???y ????ng c??ng khai")
    sold.short_description = _("???? b??n/cho thu??")
    exhaustive.short_description = _("L??n l???ch ??i kh???o s??t")

    def import_action(self, request, *args, **kwargs):
        line_count = 0
        data_type = request.POST.get('import_type')
        context = self.get_import_context_data()

        import_formats = self.get_import_formats()
        if getattr(self.get_form_kwargs, "is_original", False):
            # Use new API
            import_form = self.create_import_form(request)
        else:
            form_class = self.get_import_form_class(request)
            form_kwargs = self.get_form_kwargs(form_class, *args, **kwargs)

            if issubclass(form_class, ImportExportFormBase):
                import_form = form_class(
                    import_formats,
                    self.get_import_resource_classes(),
                    request.POST or None,
                    request.FILES or None,
                    **form_kwargs
                )
            else:
                warnings.warn(
                    "The ImportForm class must inherit from ImportExportFormBase, "
                    "this is needed for multiple resource classes to work properly. ",
                    category=DeprecationWarning
                )
                import_form = form_class(
                    import_formats,
                    request.POST or None,
                    request.FILES or None,
                    **form_kwargs
                )

        resources = list()
        if request.POST and import_form.is_valid():
            input_format = import_formats[int(import_form.cleaned_data['input_format'])]()
            if not input_format.is_binary():
                input_format.encoding = self.from_encoding
            import_file = import_form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.write_to_tmp_storage(import_file, input_format)
            # allows get_confirm_form_initial() to include both the
            # original and saved file names from form.cleaned_data
            import_file.tmp_storage_name = tmp_storage.name

            try:
                # then read the file, using the proper format-specific mode
                # warning, big files may exceed memory
                data = tmp_storage.read()
                dataset = input_format.create_dataset(data)
                # print(dataset)
            except Exception as e:
                import_form.add_error('import_file',
                                      _(f"'{type(e).__name__}' encountered while trying to read file. "
                                        "Ensure you have chosen the correct format for the file. "
                                        f"{str(e)}"))

            if not import_form.errors:
                # prepare kwargs for import data, if needed
                res_kwargs = self.get_import_resource_kwargs(request, form=import_form, *args, **kwargs)
                resource = self.choose_import_resource_class(import_form)(**res_kwargs)
                resources = [resource]

                if data_type=='Database':
                    # prepare additional kwargs for import_data, if needed
                    imp_kwargs = self.get_import_data_kwargs(request, form=import_form, *args, **kwargs)
                    result = resource.import_data(dataset, dry_run=True,
                                                  raise_errors=False,
                                                  file_name=import_file.name,
                                                  user=request.user,
                                                  **imp_kwargs)

                    context['result'] = result

                    if not result.has_errors() and not result.has_validation_errors():
                        if getattr(self.get_form_kwargs, "is_original", False):
                            # Use new API
                            context["confirm_form"] = self.create_confirm_form(
                                request, import_form=import_form
                            )
                        else:
                            confirm_form_class = self.get_confirm_form_class(request)
                            initial = self.get_confirm_form_initial(request, import_form)
                            context["confirm_form"] = confirm_form_class(
                                initial=self.get_form_kwargs(form=import_form, **initial)
                            )
                elif data_type=='K1' or data_type=='K2':
                    try:
                        print(f"open saved_search.json")
                        with open('saved_search.json', 'r', encoding='utf-8') as f:
                            searched_locations = json.load(f)

                        if request.user is not None:
                            user = request.user
                            query = Q(phone1=user.phone) or Q(user_id=user.id)
                            real = Realtor.objects.filter(query)
                            if real.first() is None:
                                Realtor.objects.create(user_id=user.id, phone1=user.phone, name=user.name, email=user.email,
                                                       address=user.address, is_cooperate=True)

                        # realtor scan and reorder
                        realtors = Realtor.objects.all()
                        realtor_dict = {}
                        for obj in realtors:
                            fone = obj.phone1
                            if len(fone) == 9 or (len(fone) == 10 and fone[0] == '0'):
                                if len(fone) == 9:
                                    fone = f'0{fone}'
                                realtor_dict[fone] = obj
                            # else:
                            #     queryset_list = Listing.objects.filter(realtor=obj)
                            #     usr_list = {}
                            #     if obj.user is not None:
                            #         usr_list = User.objects.filter(last_name=obj.user.last_name)
                            #     for usr in usr_list:
                            #         if len(usr.phone) == 10:
                            #             fone = usr.phone
                            #     for listing in queryset_list:
                            #         if (len(fone) == 10 and fone[0] == '0') or len(fone) == 9:
                            #             rel = Realtor.objects.filter(user__phone=fone)
                            #             listing.realtor = rel
                            #             listing.save()
                            #             print(f"c???p nh???t listing c?? realtor l???i sang realtor ?????y ?????: {listing.realtor}, phone {fone}")
                            #         else:
                            #             listing.delete()
                            #             print(f"x??a listing r??c do kh??ng c?? realtor ph?? h???p: {listing}")

                            #    obj.delete()
                        realtor = Realtor.objects.filter(pk=1).first()

                        # get a list of all districts in Hanoi
                        state_code = "01"
                        hanoi_district_list = district_data[state_code]
                        hanoi_districts = {}
                        for item in hanoi_district_list:  # type: dict
                            hanoi_districts[item['name']] = item['code']

                        # Open the listing file and import it into the system
                        with open(import_file.tmp_storage_name, 'r', encoding="utf-8", errors='ignore') as fp:
                            csv_reader = csv.reader(fp, delimiter=',')
                            header_dict = read_header(next(csv_reader), data_type)
                            new_listings = []
                            updated_listings = []
                            timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                            row_count = 0
                            trans_type = TransactionType.SELL
                            house_type = HouseType.TOWN_HOUSE
                            road_type = RoadType.ALLEY_TRIBIKE
                            direction = ""
                            reward = 100
                            bonus_rate = 3
                            desc = ""
                            shop_house = "shophouse"
                            biet_thu = "bt"
                            lien_ke = "lk"
                            dich_vu = "dv"
                            thap_tang = "tt"
                            lo = "l??"
                            chung_cu = "chung c??"
                            cao_tang = "ct"
                            tap_the = "t???p th???"
                            du_an = "d??? ??n"
                            extra_data = ""

                            # start reading and scanning the file from the bottom up
                            for row in reversed(list(csv_reader)):
                                row_count += 1
                                line_count = csv_reader.line_num - row_count + 1

                                # read state, district information
                                try:
                                    if data_type == 'K1':
                                        state_name = 'H?? N???i'
                                    else:
                                        state_name = row[header_dict['thanh-pho']]
                                    district = row[header_dict['quan']]
                                    if not district:
                                        continue
                                    if district in hanoi_districts:
                                        district_code = hanoi_districts[district]
                                    else:
                                        # logger.info(f"District code not found. Continue in line {line_count}")
                                        continue
                                except ValueError:
                                    state_name = 'H?? N???i'
                                    pass

                                # Read information about date and time listing
                                created_date = row[header_dict['tgian']]
                                # created = datetime.now(tz=timezone).date()
                                try:
                                    if data_type == "K1":
                                        created = datetime.strptime(created_date, '%d/%m/%Y %H:%M:%S')
                                    elif data_type == "K2":
                                        created = datetime.strptime(created_date, '%d/%m/%Y %H:%M')
                                    created_date = created.replace(tzinfo=timezone).date()

                                except ValueError:
                                    logger.info(f"error date create {created_date}")
                                    created_date = datetime.now(tz=timezone).date()

                                # Read information about area
                                area = row[header_dict['dt']]
                                try:
                                    # area = float(row[header_dict['dt']].replace('c4', ''))
                                    if not area or area == '#VALUE!':
                                        continue
                                    area = Decimal(area.replace(',', '.').replace(' ', ''))
                                except ValueError:
                                    logger.info(f"error area  {area}")
                                    pass

                                # Read information about floor
                                try:
                                    if data_type != "K1":
                                        floor = row[header_dict['so-tang']]
                                    else:
                                        floor = None
                                    if floor is not None:
                                        floor = Decimal(floor.replace(',', '.').replace(' ', ''))
                                        if floor == 0:
                                            house_type = HouseType.LAND
                                        elif floor == 1:
                                            house_type = HouseType.LOFT_HOUSE
                                        else:
                                            house_type = HouseType.TOWN_HOUSE
                                except ValueError:
                                    logger.info(f"error floor  {floor}")
                                    pass

                                # Read information about width
                                try:
                                    if data_type != "K1":
                                        width = row[header_dict['mat-tien']]
                                    else:
                                        width = 0
                                    if width is not None and not width == 0:
                                        width = Decimal(width.replace(' ', '').replace(',', '.'))
                                except ValueError:
                                    logger.info(f"error width  {width}")
                                    continue

                                # Read real estate price information
                                price = row[header_dict['gia']]
                                try:
                                    if price == '#VALUE!' or price == '':
                                        continue
                                    price_k2 = price
                                    price = price.split(' ')[0]
                                    price = Decimal(price.replace(',', '.').replace(' ', ''))
                                    if not price:
                                        continue
                                    if price > 1000000 and area < 10000000:
                                        price = Decimal(price / 1000000)
                                    elif price > 100000 and area < 1000000:
                                        price = Decimal(price / 100000)
                                    elif price > 10000 and area < 100000:
                                        price = Decimal(price / 10000)
                                    elif price > 1000 and area < 10000:
                                        price = Decimal(price / 1000)
                                    if float(area) > 0:
                                        price_per_area = Decimal(float(price) / float(area) * 1000)
                                    else:
                                        price_per_area = None
                                except ValueError:
                                    logger.info(f"error price {price}")
                                    pass

                                # Read information about the current state of the sale and set priority, show/hide into web by district
                                status = row[header_dict['hien-trang']]
                                try:
                                    if status == 'C??n b??n' or status == 'Chu???n' or status == 'Ch??? duy???t' or status == 'Chim tr???i c?? b???':
                                        status = Status.SELLING
                                        is_published = True
                                    elif status == '???? b??n' or status == '???? c???c':
                                        status = Status.SOLD
                                        is_published = False
                                    elif status == 'D???ng b??n' or status == 'T???m d???ng b??n':
                                        status = Status.STOP_SELLING
                                        is_published = False
                                    elif status == 'H??? ch??o':
                                        status = Status.SALE
                                        is_published = True
                                    else:
                                        status = Status.SOLD
                                        is_published = False
                                    # 008 Q. Ho??ng Mai,009 Q. Thanh Xu??n, 020 H. Thanh Tr??, 278 H. Thanh Oai, 268 Q. H?? ????ng
                                    if district_code == '008' or district_code == '009' or district_code == '020' or district_code == '278' or district_code == '268':
                                        priority = 8
                                    else:
                                        priority = 9
                                except ValueError:
                                    logger.info(f"error status {status}")
                                    pass

                                # ph??n t??ch ch???c v???, t??n ?????u ch???
                                dau_chu = row[header_dict['dau-chu']]
                                try:
                                    dau_chu_chu_thuong = dau_chu.lower()
                                    machucvu = dau_chu_chu_thuong.split(' ')[0]
                                    position = Position.EXPERT_HOME
                                    if "?????u ch???" in dau_chu_chu_thuong or machucvu == '??c':
                                        position = Position.EXPERT_HOME
                                    if "b?? t?????c" in dau_chu_chu_thuong or machucvu == 'bt':
                                        position = Position.REGIONAL_DIRECTOR
                                    if "tr?????ng ph??ng" in dau_chu_chu_thuong or machucvu == 'tp':
                                        position = Position.MANAGER
                                except ValueError:
                                    continue

                                # read ????n v???
                                don_vi = row[header_dict['don-vi']]
                                try:
                                    workplace = Workplace.TGNP
                                    nguon = "Th??? gi???i Nh?? ph???"
                                    if don_vi is None or don_vi == "":
                                        workplace = Workplace.THIENKHOI
                                        nguon = "Thi??n kh??i"
                                    else:
                                        workplace = Workplace.NHAPHO
                                        nguon = "Nh?? ph???"
                                except ValueError:
                                    continue

                                # read ngu???n & hoa h???ng
                                try:
                                    if data_type != 'K1':
                                        nguon = row[header_dict['nguon']]
                                        hoa_hong = row[header_dict['hoa-hong']]
                                        extra_add = f' Ngu???n {nguon}, hoa h???ng {hoa_hong}.'
                                    else:
                                        hoa_hong = ''
                                        extra_add = f' Ngu???n {nguon}, hoa h???ng 3%, x??c minh l???i v???i ?????u ch??? {dau_chu}.'
                                    num_reward = 100
                                    if (not (hoa_hong.split(' ')[0] and hoa_hong.split(' ')[0].strip())):
                                        num_reward = 100
                                        bonus_rate = 3
                                    if 3 < int(num_reward) < 10000:
                                        reward = num_reward
                                    elif int(num_reward) > 0:
                                        bonus_rate = num_reward
                                    else:
                                        bonus_rate = 3
                                except ValueError:
                                    extra_add = f'Ngu???n TGNP, hoa h???ng 3%, x??c minh l???i v???i ?????u ch??? {dau_chu}.'

                                # Read information about specialist phone number. Add realtor from phone list
                                phone = row[header_dict['sdt']].strip()
                                try:
                                    if '-' in phone:
                                        phones = phone.split('-')
                                    else:
                                        phones = phone.split(' ')
                                    if len(phones) > 1 and (phones[1] == 9 or phones[1] == 10):
                                        phone2 = phones[1]
                                    else:
                                        phone2 = ""
                                    phone = phones[0]

                                    if not phone.isalnum():
                                        realtor_dict[phone] = Realtor.objects.filter(pk=1).first()
                                        logger.info(f"Phone invalid. Continue in line {line_count}")
                                        phone = '0964399436'
                                        #continue
                                    elif len(phone) == 9 or (len(phone) == 10 and phone[0] == '0'):
                                        # update, delete user, realtor
                                        tmp_phone = phone
                                        if len(phone) == 9:
                                            phone = f'0{phone}'
                                        query = Q(phone=phone) | Q(phone=tmp_phone)
                                        if phone2 is not None or not phone2 == "":
                                            query = query | Q(phone=phone2)

                                        user_tmp = User.objects.filter(query).first()
                                        email = f'{phone}@gmail.com'
                                        story = f'{dau_chu}, {phone}, {don_vi}.'

                                        if phone not in realtor_dict:
                                            new_realtor = Realtor.objects.create(user=user_tmp, name=dau_chu, phone1=phone,
                                                                                 phone2=phone2, email=email, story=story,
                                                                                 position=position, title=Title.MASTER,
                                                                                 level=5,
                                                                                 workplace=workplace, department=don_vi,
                                                                                 hire_date=datetime.now(
                                                                                     tz=timezone))
                                            realtor_dict[phone] = new_realtor
                                            realtor = new_realtor
                                            print(f"t???o realtor: {new_realtor} ch??a c??")
                                        elif user_tmp != realtor_dict[phone].user:
                                            realtor = realtor_dict[phone]
                                            realtor.user = user_tmp
                                            realtor.save()
                                            print(f"c???p nh???t user: {user_tmp} cho realtor {realtor}")
                                        real = Realtor.objects.filter(Q(phone1=tmp_phone) | Q(phone2=tmp_phone) | Q(phone1=phone) | Q(phone2=phone))
                                        if phone2 is not None or not phone2 == "":
                                            real = real.filter(Q(phone1=phone2) | Q(phone2=phone2))
                                        realtor = real.first()
                                except ValueError:
                                    logger.info(f"error phone {phone}")

                                # get address and street
                                addr = row[header_dict['dia-chi']].strip().replace('.', '/').replace(' , ', ', ').replace(
                                    ',',
                                    '/').replace(
                                    'S??? ', '').replace('??', ' ')
                                street = row[header_dict['pho']]
                                try:
                                    so_nha = addr.split(' ')
                                    deep_address = so_nha[0].split('/')
                                    if "+" in deep_address:
                                        deep_address = deep_address.split('+')
                                    if len(street) > 0:
                                        full_addr = f'{addr}, {street}, {district}, {state_name}'
                                    else:
                                        lensonha = int(len(so_nha[0]))
                                        street = addr[lensonha:].replace('(', '').replace(')', '').replace('/', '').replace(
                                            '  ',
                                            '')
                                        street = street.translate(street.maketrans('', '', digits))
                                        full_addr = f'{addr}, {district}, {state_name}'
                                    full_addr = full_addr.replace(' TT ', ' t???p th??? ').replace('CCCC',
                                                                                               'Chung c?? cao c???p').replace(
                                        'CCMN', 'Chung c?? mini').replace('CC ', 'Chung c?? ')
                                    add_search_map = f'{deep_address[0]} {street}, {district}, {state_name}'
                                    add_search_map = add_search_map.replace('  ', ' ')
                                except ValueError:
                                    logger.info(f'error address {full_addr}')

                                # search location on map
                                try:
                                    listing_loc = Point(105.83549388560711, 20.976795401917798)
                                    if add_search_map in searched_locations:
                                        if searched_locations[add_search_map]:
                                            listing_loc = Point(searched_locations[add_search_map][0],
                                                                searched_locations[add_search_map][1])
                                    else:
                                        # if api_key:
                                        # geolocator = GeocodeEarth(api_key=api_key)
                                        geolocator = Nominatim(user_agent="thegioinhaphovietnam.com.vn")
                                        # GeocodeEarth.geocoders.options.default_user_agent = "my-application"
                                        hanoi_bounds = ((21.097341, 105.929947), (20.920105, 105.702667))
                                        location = geolocator.geocode(add_search_map, timeout=None, bounded=True,
                                                                      viewbox=hanoi_bounds)
                                        # location = geolocator.geocode(add_search_map, timeout=None)
                                        if location and location.point:
                                            listing_loc = Point(location.point.longitude, location.point.latitude)
                                            searched_locations[add_search_map] = [location.point.longitude,
                                                                                  location.point.latitude]
                                        else:
                                            searched_locations[add_search_map] = None
                                except ValueError:
                                    logger.info(f"error search location {add_search_map}")

                                # get ?????c ??i???m b??s, title
                                title_hot = ''
                                desc = row[header_dict['dac-diem']].replace('N', 'n').replace('K', 'k').replace('B',
                                                                                                                'b').replace(
                                    'X', 'x').replace('D', 'd') \
                                    .replace('M', 'm').replace('G', 'g').replace('??', '??').replace('T', 't').replace('G',
                                                                                                                     'g') \
                                    .replace('??', '??').replace('??', '??').replace('P', 'p').replace('C', 'c')
                                try:
                                    if biet_thu in full_addr.lower():
                                        house_type = HouseType.VILLA
                                        road_type = RoadType.ALLEY_CAR_2
                                    elif shop_house in full_addr.lower():
                                        house_type = HouseType.SHOP_HOUSE
                                        road_type = RoadType.ALLEY_CAR_2
                                    elif lien_ke in full_addr.lower() or dich_vu in full_addr.lower() or lo in full_addr.lower() or du_an in full_addr.lower() or desc == 'Li???n K???' or thap_tang in full_addr.lower():
                                        house_type = HouseType.PLOT
                                        road_type = RoadType.ALLEY_CAR_2
                                    elif "chung c?? mini" in full_addr.lower():
                                        house_type = HouseType.APARTMENT
                                        road_type = RoadType.ALLEY_CAR
                                    elif cao_tang in full_addr.lower() or chung_cu in full_addr.lower() or " tt " in full_addr.lower() or tap_the in full_addr.lower():
                                        full_addr = full_addr.replace(' TT ', ' t???p th??? ').replace('CCCC',
                                                                                                   'Chung c?? cao c???p')
                                        house_type = HouseType.APARTMENT
                                        road_type = RoadType.ALLEY_CAR_2

                                    if '?????t d??? ??n' in desc:
                                        house_type = HouseType.PLOT
                                        road_type = RoadType.ALLEY_CAR_2
                                        trans_type = TransactionType.PROJECT
                                    elif 'chung c??' in desc:
                                        house_type = HouseType.APARTMENT
                                        road_type = RoadType.ALLEY_CAR_2
                                    elif 'ng?? ?? t??' in desc:
                                        house_type = HouseType.TOWN_HOUSE
                                        road_type = RoadType.ALLEY_CAR
                                        title_hot = 'ng?? ?? t??'
                                    elif 'ng?? 3 g??c' in desc:
                                        house_type = HouseType.TOWN_HOUSE
                                        road_type = RoadType.ALLEY_TRIBIKE
                                    elif 'ng?? xe m??y' in desc:
                                        house_type = HouseType.TOWN_HOUSE
                                        road_type = RoadType.ALLEY_BIKE
                                    elif 'kinh doanh' in desc:
                                        road_type = RoadType.ALLEY_CAR
                                        title_hot = 'kinh doanh t???t'

                                    if (len(deep_address) == 1 and deep_address[0].isalnum()) or ('m???t ph???' in desc):
                                        house_type = HouseType.STREET_HOUSE
                                        road_type = RoadType.ALLEY_CAR_2

                                    if len(desc) > 0:
                                        extra_data = f'B???t ?????ng s???n {desc}. {full_addr}.\n' + extra_data
                                except ValueError:
                                    logger.info(f"error dac-diem {desc}")

                                # Ph??n t??ch c?? ph??p th??ng s??? ????? l???y di???n t??ch, s??? t???ng, m???t ti???n t??? file ngu???n nh?? ph???
                                if data_type == "K1":
                                    try:
                                        encoded_num = row[header_dict['thong-so']].replace('  ', ' ')
                                        splitter = encoded_num.strip().split(' ')
                                        floor = 0
                                        floor_code = splitter[1]
                                        floor_code = slugify(
                                            floor_code.lower().replace('??', 'd').replace('???', 'a').replace('t', '')
                                            .replace('c4', 'c').replace(' ', ''))
                                        if floor_code == 'c' or floor_code == 'cap':
                                            floor = 1
                                            house_type = HouseType.LOFT_HOUSE
                                        elif floor_code == 'da' or floor_code == 'd':
                                            floor = 0
                                            house_type = HouseType.LAND
                                        else:
                                            floor = int(floor_code)

                                        splitter_len = len(splitter)
                                        if splitter_len == 4 or splitter_len == 3:
                                            width = splitter[2].replace(',', '.').replace(' ', '').split('/')
                                            width = Decimal(width[0].replace(',', '.').replace(' ', ''))
                                        else:
                                            width = None

                                    except ValueError:
                                        logger.info(
                                            f"Cannot decode encoded_num {encoded_num}. Continue in line {line_count}")

                                # L???y ti??u ????? nh???p t??? file
                                title = row[header_dict['tieude']]
                                if title is None or title == "":
                                    title = f'B??n {get_short_title_from_house_type(house_type)} {title_hot} {street} {get_district_name(district_code)} '
                                    if area >= 30:
                                        title += f'{area:.0f}m '
                                    if house_type == HouseType.APARTMENT or house_type == HouseType.CONDO_TEL or house_type == HouseType.SERVICE_APARTMENT or house_type == HouseType.PENT_HOUSE:
                                        title += f't???ng {floor:.0f} gi?? '
                                    elif int(floor) > 3:
                                        title += f'{floor:.0f} t???ng '
                                    if price % 1 == 0:
                                        title += f'{price:.0f} t???'
                                    else:
                                        title += f'{price:.1f} t???'
                                title = title.upper().replace('  ', ' ')

                                # L???y m?? t??? b??s ?????u ch??? nh???p t??? file
                                extra_data = row[header_dict['motadauchu']]
                                if extra_data is None or extra_data == "":
                                    if data_type == 'K1':
                                        extra_data = f'{addr} {street} {encoded_num} {price} t??? {district} {dau_chu} {don_vi} {phone} {desc}.\n{extra_add}'
                                    else:
                                        extra_data = f'{addr} {area} {floor} {width} {price_k2} {district} {dau_chu} {don_vi} {phone} HH {hoa_hong}.\n{extra_add}'

                                starter = get_house_type_short(house_type)
                                code = f'{starter}{data_type}{created_date.strftime("%y%m")}{int(area)}{price}'
                                new_listing = Listing(user=user, realtor=realtor, code=code, status=status, title=title,
                                                      street=street, address=full_addr, area=area,
                                                      transaction_type=trans_type,
                                                      house_type=house_type, road_type=road_type, date_created=created_date,
                                                      direction=direction, price=price, priority=priority,
                                                      reward_person_mobile=phone, reward=reward, bonus_rate=bonus_rate,
                                                      extra_data=extra_data, state=state_code, district=district_code,
                                                      is_published=is_published,
                                                      width=width, floors=floor, average_price=price_per_area, length=None,
                                                      lane_width=None,
                                                      location=listing_loc)

                                # L???y m?? t??? n???i dung b??s nh???p t??? file
                                description = row[header_dict['mota']]
                                if description is None or description == "":
                                    new_listing.description = render_to_string('listings/defaultDescription.html',
                                                                               context={"listing": new_listing,
                                                                                        "desc": desc}).replace('  ', ' ')
                                else:
                                    new_listing.description = description

                                query = (Q(address__contains=so_nha[0]) & Q(area=area) & Q(floors=floor) & Q(
                                    width=width) & Q(
                                    price=price)) | \
                                        (Q(address__contains=so_nha[0]) & Q(area=area) & Q(street=street) & Q(
                                            state=state_code))
                                querylist_list = Listing.objects.filter(
                                    Q(code=code) | Q(address=full_addr) | query).order_by(
                                    '-date_created')
                                # N???u kho ???? t???n t???i b??s
                                if querylist_list.exists():
                                    count_update = 0
                                    listing_fisrt = None
                                    # if querylist_list.count() > 0:
                                    #    print(f"row {line_count}: kho ??ang c?? {querylist_list.count()} b??s: {new_listing}")
                                    # duy???t to??n b??? t??m c??c listing tr??ng l???p ??ang c?? trong kho
                                    for listing in querylist_list:
                                        if listing is not None:
                                            # logger.info(f"row {line_count}: listing {listing}, count_update {count_update}")
                                            # Ki???m tra listing ti???p theo, n???u c?? h??n th?? x??a, m???i h??n th?? c???p nh???t
                                            if listing_fisrt is None:
                                                listing_fisrt = listing
                                            # n???u listing m???i import c?? h??n listing trong kho th?? ch??? ?????y listing n??y sang b???ng listing history

                                            if listing.date_created is None:
                                                listing.date_created = new_listing.date_created
                                            if listing.date_created > new_listing.date_created:
                                                querylist_listhistory = ListingHistory.objects.filter(
                                                    listing_id=listing_fisrt.id,
                                                    date_created=new_listing.date_created)
                                                # Ki???m tra trong listing history ???? c?? tr??ng l???p ch??a, n???u ch??a c?? th?? ?????y v??o, n???u c?? r???i b??? qua
                                                if not querylist_listhistory.exists() and count_update >= 1:
                                                    new_listhis = ListingHistory.objects.create(listing=listing_fisrt,
                                                                                                user=new_listing.user,
                                                                                                realtor=new_listing.realtor,
                                                                                                area=new_listing.area,
                                                                                                floors=new_listing.floors,
                                                                                                width=new_listing.width,
                                                                                                address=new_listing.address,
                                                                                                bathrooms=new_listing.bathrooms,
                                                                                                bedrooms=new_listing.bedrooms,
                                                                                                price=new_listing.price,
                                                                                                reward_person_mobile=new_listing.reward_person_mobile,
                                                                                                reward_person=new_listing.reward_person,
                                                                                                extra_data=new_listing.extra_data,
                                                                                                warehouse=data_type,
                                                                                                date_created=new_listing.date_created)
                                                    new_listhis.save()
                                                    logger.info(f"row {line_count}: t???o m???i l???ch s??? b??s {new_listhis} t??? listing import c?? h??n {new_listing}, b??s g???c {listing_fisrt}")
                                            # N???u listing ????a v??o l?? m???i nh???t l?? l???n ?????u th?? c???p nh???t th??ng tin m???i cho listing
                                            elif listing.date_created == new_listing.date_created:
                                                # C???p nh???t th??ng tin m???i nh???t cho listing ??ang c??
                                                if listing.priority == 1 or listing.priority == 2:
                                                    if listing_fisrt.user is None:
                                                        listing_fisrt.user = new_listing.user
                                                    listing_fisrt.realtor = new_listing.realtor
                                                    listing_fisrt.status = new_listing.status
                                                    listing_fisrt.street = new_listing.street
                                                    listing_fisrt.address = new_listing.address
                                                    listing_fisrt.location = new_listing.location
                                                    listing_fisrt.house_type = new_listing.house_type
                                                    listing_fisrt.road_type = new_listing.road_type
                                                    listing_fisrt.reward_person = new_listing.reward_person
                                                    listing_fisrt.reward_person_mobile = new_listing.reward_person_mobile
                                                    listing_fisrt.extra_data = new_listing.extra_data
                                                    listing_fisrt.date_created = new_listing.date_created
                                                    listing_fisrt.is_published = new_listing.is_published
                                                    listing_fisrt.save()
                                                    # logger.info(f"row {line_count}: c???p nh???t {listing} prior {listing.priority} t??? {new_listing}")
                                                else:
                                                    listing_fisrt.user = new_listing.user
                                                    listing_fisrt.realtor = new_listing.realtor
                                                    listing_fisrt.house_type = new_listing.house_type
                                                    listing_fisrt.road_type = new_listing.road_type
                                                    listing_fisrt.status = new_listing.status
                                                    listing_fisrt.area = new_listing.area
                                                    listing_fisrt.floors = new_listing.floors
                                                    listing_fisrt.width = new_listing.width
                                                    listing_fisrt.price = new_listing.price
                                                    listing_fisrt.title = new_listing.title
                                                    listing_fisrt.description = new_listing.description
                                                    listing_fisrt.reward_person = new_listing.reward_person
                                                    listing_fisrt.reward_person_mobile = new_listing.reward_person_mobile
                                                    listing_fisrt.extra_data = new_listing.extra_data
                                                    listing_fisrt.priority = new_listing.priority
                                                    listing_fisrt.street = new_listing.street
                                                    listing_fisrt.address = new_listing.address
                                                    listing_fisrt.location = new_listing.location
                                                    listing_fisrt.status = new_listing.status
                                                    listing_fisrt.date_created = new_listing.date_created
                                                    listing_fisrt.is_published = new_listing.is_published
                                                    listing_fisrt.save()
                                                    # logger.info(f"row {line_count}: c???p nh???t {listing.code} ??u ti??n {listing.priority} t??? {new_listing}")
                                            elif listing.date_created < new_listing.date_created:
                                                querylist_listhistory = ListingHistory.objects.filter(listing=listing_fisrt,
                                                                                                      date_created=listing.date_created)
                                                # Ki???m tra trong listing history ???? c?? tr??ng l???p ch??a, n???u ch??a c?? th?? ?????y v??o, n???u c?? r???i b??? qua
                                                if not querylist_listhistory.exists() and count_update >= 1:
                                                    # ?????y th??ng tin listing c?? v??o l???ch s??? listing
                                                    new_listhis = ListingHistory.objects.create(listing=listing_fisrt,
                                                                                                user=listing.user,
                                                                                                address=listing.address,
                                                                                                realtor=listing.realtor,
                                                                                                area=listing.area,
                                                                                                floors=listing.floors,
                                                                                                width=listing.width,
                                                                                                bathrooms=listing.bathrooms,
                                                                                                bedrooms=listing.bedrooms,
                                                                                                price=listing.price,
                                                                                                reward_person_mobile=listing.reward_person_mobile,
                                                                                                reward_person=listing.reward_person,
                                                                                                extra_data=listing.extra_data,
                                                                                                warehouse=data_type,
                                                                                                date_created=listing.date_created)
                                                    new_listhis.save()
                                                    logger.info(
                                                        f"row {line_count}: ?????y th??ng tin listing {listing} c?? h??n tr??n server v??o l???ch s??? listing {new_listhis}")
                                                # C???p nh???t th??ng tin m???i nh???t cho listing ??ang c??
                                                if listing.priority == 1 or listing.priority == 2:
                                                    if listing_fisrt.user is None:
                                                        listing_fisrt.user = new_listing.user
                                                    listing_fisrt.realtor = new_listing.realtor
                                                    listing_fisrt.status = new_listing.status
                                                    listing_fisrt.street = new_listing.street
                                                    listing_fisrt.address = new_listing.address
                                                    listing_fisrt.location = new_listing.location
                                                    listing_fisrt.code = new_listing.code
                                                    listing_fisrt.house_type = new_listing.house_type
                                                    listing_fisrt.road_type = new_listing.road_type
                                                    listing_fisrt.reward_person = new_listing.reward_person
                                                    listing_fisrt.reward_person_mobile = new_listing.reward_person_mobile
                                                    listing_fisrt.extra_data = new_listing.extra_data
                                                    listing_fisrt.date_created = new_listing.date_created
                                                    listing_fisrt.is_published = new_listing.is_published
                                                    listing_fisrt.save()
                                                    # logger.info(f"row {line_count}: c???p nh???t {listing} prior {listing.priority} t??? {new_listing}")
                                                else:
                                                    listing_fisrt.user = new_listing.user
                                                    listing_fisrt.realtor = new_listing.realtor
                                                    listing_fisrt.house_type = new_listing.house_type
                                                    listing_fisrt.road_type = new_listing.road_type
                                                    listing_fisrt.status = new_listing.status
                                                    listing_fisrt.area = new_listing.area
                                                    listing_fisrt.floors = new_listing.floors
                                                    listing_fisrt.width = new_listing.width
                                                    listing_fisrt.price = new_listing.price
                                                    listing_fisrt.title = new_listing.title
                                                    listing_fisrt.description = new_listing.description
                                                    listing_fisrt.reward_person = new_listing.reward_person
                                                    listing_fisrt.reward_person_mobile = new_listing.reward_person_mobile
                                                    listing_fisrt.extra_data = new_listing.extra_data
                                                    listing_fisrt.priority = new_listing.priority
                                                    listing_fisrt.street = new_listing.street
                                                    listing_fisrt.address = new_listing.address
                                                    listing_fisrt.location = new_listing.location
                                                    listing_fisrt.code = new_listing.code
                                                    listing_fisrt.status = new_listing.status
                                                    listing_fisrt.date_created = new_listing.date_created
                                                    listing_fisrt.is_published = new_listing.is_published
                                                    if Listing.objects.filter(code=listing_fisrt.code).exists():
                                                        listing_fisrt.code = new_listing.code + deep_address[0]
                                                    listing_fisrt.save()
                                                    # logger.info(f"row {line_count}: c???p nh???t {listing.code} prior {listing.priority} t??? {new_listing}")
                                            if count_update >= 1 and listing.id is not None:
                                                findlisthistory = ListingHistory.objects.filter(listing=listing)
                                                if findlisthistory.exists():
                                                    for hislist in findlisthistory:
                                                        hislist.listing = listing_fisrt
                                                        hislist.save()
                                                else:
                                                    qrlist = Listing.objects.filter(address=listing.address)
                                                    if qrlist.count() > 1:
                                                        listing.delete()
                                                        print(f"row {line_count}: x??a listing th???a: {listing}")

                                        count_update += 1
                                else:
                                    new_listing.save()
                                    # print(f"row {line_count}: t???o m???i listing: {new_listing} ch??a c??")

                    except Exception as ex:
                        print(f"L???i ??? d??ng: {line_count} type {type(ex)}")
                        print_trace(ex)
                    finally:
                        print(f'Read {row_count} lines')
                        with open('saved_search.json', 'w', encoding='utf-8') as f:
                            json.dump(searched_locations, f, ensure_ascii=False)

                if not self.has_import_permission(request):
                    raise PermissionDenied
        else:
            res_kwargs = self.get_import_resource_kwargs(request, form=import_form, *args, **kwargs)
            resource_classes = self.get_import_resource_classes()
            resources = [resource_class(**res_kwargs) for resource_class in resource_classes]

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Import")
        context['form'] = import_form
        context['opts'] = self.model._meta
        context['media'] = self.media + import_form.media
        context['fields_list'] = [
            (resource.get_display_name(), [f.column_name for f in resource.get_user_visible_fields()])
            for resource in resources
        ]

        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name],
                                context)

    def export_action(self, request, *args, **kwargs):
        if not self.has_export_permission(request):
            raise PermissionDenied

        if getattr(self.get_export_form, 'is_original', False):
            form_type = self.get_export_form_class()
        else:
            form_type = self.get_export_form()
        formats = self.get_export_formats()
        form = form_type(formats, self.get_export_resource_classes(), request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()
            content_type = file_format.get_content_type()

            if request.POST.get('export_type') == 'Database':
                queryset = self.get_export_queryset(request)
                export_data = self.get_export_data(
                    file_format, queryset, request=request, encoding=self.to_encoding, export_form=form,
                )
                response = HttpResponse(export_data, content_type=content_type)
                response['Content-Disposition'] = 'attachment; filename="%s"' % (
                    self.get_export_filename(request, queryset, file_format),
                )

                post_export.send(sender=None, model=self.model)
                return response
            elif request.POST.get('export_type') == 'Facebook':
                output = io.StringIO()
                writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
                headers = prepare_fb_headers()
                writer.writerow(headers)
                for listing in Listing.objects.all():
                    row = []
                    for val in prepare_fb_listing_data(listing):
                        row.append(val[1])
                    writer.writerow(row)
                output.seek(0)
                resp = HttpResponse(output.read(), content_type=content_type)
                resp[
                    'Content-Disposition'] = f'filename=Listing_export_facebook-{datetime.today().strftime("%Y-%m-%d")}.csv'
                output.close()
                return resp

        context = self.get_export_context_data()
        context.update(self.admin_site.each_context(request))

        context['title'] = _("Export")
        context['form'] = form
        context['opts'] = self.model._meta
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.export_template_name],
                                context)


class ListingHistoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('TH??NG TIN CHUY??N VI??N', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('TH??NG TIN B???T ?????NG S???N', {'fields': (
            ('listing','address'),
            'extra_data',
            ('area', 'floors', 'width'), ('price', 'bedrooms', 'bathrooms'),
            ('warehouse', 'date_created'), ('reward_person', 'reward_person_mobile'),
        )}),
    )

    list_display = ('listing', 'area', 'floors', 'width', 'price', 'warehouse', 'date_created',)
    list_display_links = ('listing',)
    list_filter = (
        # ('area', RangeNumericFilter),
        # ('floors', RangeNumericFilter),
        # ('width', RangeNumericFilter),
        # ('price', RangeNumericFilter),
        # ('bedrooms', RangeNumericFilter),
        ('date_created', DateFieldListFilter),
    )
    list_editable = ()
    search_fields = ('id', 'address', 'date_created', 'reward_person', 'reward_person_mobile','extra_data','warehouse')
    autocomplete_fields = ['listing','user', 'realtor']
    list_per_page = 200
    inlines = []
    # usual admin stuff goes here
    inline_type = 'tabular'  # or could be 'stacked'
    inline_reverse = ['listing']
    actions = []
    form = ListingAdminForm
    ordering = ('-date_created',)
    #filter_horizontal = ('realtor')

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/listing.js', 'admin/js/filepond-4.28.2.min.js',
              'admin/js/micromodal-0.4.6.min.js')
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css', 'admin/css/filepond.min.css')
        }

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(ListingHistoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        realtor_list = Realtor.objects.filter(user=request.user)
        if realtor_list is not None:
            form.base_fields['realtor'].initial = realtor_list.first()
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user',
            'realtor'
        }
        excludes = ('reward_person_mobile', 'extra_data')
        if request.user.is_superuser:
            form.base_fields['user'].disabled = True
        elif request.user.is_staff:
            for exc in excludes:
                if exc in form.base_fields:
                    form.base_fields[exc].widget = forms.HiddenInput()
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        else:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        return form

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.is_staff:
            queryset = super().get_queryset(request)
            return queryset
        else:
            queryset_list = Listing.objects.order_by('-date_update')
            query = Q(realtor__user=request.user.id)
            query = query | Q(user=request.user)
            queryset_list = queryset_list.filter(query)
            return queryset_list


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingHistory, ListingHistoryAdmin)
