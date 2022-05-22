import fractions

from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.contrib.admin import FieldListFilter, BooleanFieldListFilter, DateFieldListFilter
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django import forms
from django.http import HttpRequest, JsonResponse

from FunctionModule.listings.import_csv import handle_import, logger
from .filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter, IsWithinRangeFilter, \
    SimpleDropdownFilter, AreaFilter
from .forms import ListingAdminForm, ImportListingForm, ImageForm, ImageFormSet
from .models import Listing, ListingImage, ListingVideo, ContractImage, ListingHistory
from .choices import district_default_choices
from ..realtors.models import Realtor
from django.db.models import Q
from fractions import *


class ContractPhotoAdmin(admin.TabularInline):
    model = ContractImage
    verbose_name = "ẢNH HỢP ĐỒNG TRÍCH THƯỞNG & PHIẾU KHẢO SÁT BĐS"


class ListingPhotoAdmin(admin.TabularInline):
    model = ListingImage
    verbose_name = "HÌNH ẢNH CHỤP BĐS"
    form = ImageForm
    formset = ImageFormSet

    max_num = 20
    extra = 0


class ListingVideoAdmin(admin.TabularInline):
    model = ListingVideo
    extra = 1
    verbose_name = "VIDEO QUAY BĐS"


class ListingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN GIAO DỊCH', {'fields': (
            ('transaction_type', 'house_type'),)}),
        ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
            ('title', 'code'), ('description', 'extra_data'),
            ('area', 'floors', 'width'), ('price', 'registration_type', 'road_type'),
        )}),
        ('ĐỊA CHỈ & VỊ TRÍ BĐS', {'fields': (
            ('state', 'district', 'ward'), ('street', 'address', 'location'))}),
        ('TRẠNG THÁI ĐĂNG TIN', {
            'fields': (('status', 'priority','list_date'), ('is_published', 'is_verified', 'is_exclusive'),)}),
    )

    list_display = (
    'address', 'area', 'floors', 'width', 'price', 'average_price', 'road_type', 'house_type', 'code', 'status',
     'district',)
    list_display_links = ('code', 'address',)
    list_filter = (
        ('status', ChoiceDropdownFilter),
        ('house_type', ChoiceDropdownFilter),
        ('road_type', ChoiceDropdownFilter),
        #('floors', ChoiceDropdownFilter),
        ('registration_type', ChoiceDropdownFilter),
        #('realtor', RelatedDropdownFilter),
        ('transaction_type', ChoiceDropdownFilter),
        ('list_date', DateFieldListFilter),
        ('is_published', BooleanFieldListFilter),
        ('is_advertising', BooleanFieldListFilter),
        #AreaFilter,
    )
    #advanced_filter_fields = ('status', ('house_type', 'road_type'))
    list_editable = ('price',)
    search_fields = (
    'id', 'title', 'code', 'address', 'area', 'price', 'house_type', 'road_type', 'urban_area', 'street', 'ward',
    'district', 'state', 'list_date',)
    list_per_page = 200
    inlines = [ListingPhotoAdmin, ListingVideoAdmin, ContractPhotoAdmin]
    actions = ['make_published', 'unpublished']
    form = ListingAdminForm
    ordering = ('-list_date',)

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/listing.js', 'admin/js/filepond-4.28.2.min.js',
              'admin/js/micromodal-0.4.6.min.js')
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css', 'admin/css/filepond.min.css')
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
            queryset_list = Listing.objects.order_by('-list_date')
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
        self.message_user(request, f'Đã đổi trạng thái cho {updated} căn')

    def unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Đã đổi trạng thái cho {updated} căn')


class ListingHistoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
            'listing', ('warehouse', 'list_date'), ('reward_person', 'reward_person_mobile', 'extra_data'),
            ('area', 'floors', 'width'), ('price', 'bedrooms', 'bathrooms'),
        )}),
    )

    list_display = ('listing', 'area', 'floors', 'width', 'price', 'bedrooms', 'bathrooms', 'warehouse', 'list_date',)
    list_display_links = ('listing',)
    list_filter = (
        ('list_date', DateFieldListFilter),
        ('listing', ChoiceDropdownFilter),
    )
    list_editable = ()
    search_fields = ('id', 'area', 'price', 'list_date',)
    list_per_page = 200
    inlines = []
    actions = []
    form = ListingAdminForm
    ordering = ('-list_date',)

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
            queryset_list = Listing.objects.order_by('-list_date')
            query = Q(realtor__user=request.user.id)
            query = query | Q(user=request.user)
            queryset_list = queryset_list.filter(query)
            return queryset_list


@admin.site.register_view('listings/listing/import-listing')
def import_csv_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = ImportListingForm(request.POST, request.FILES)
        if form.is_valid():
            file: UploadedFile = form.cleaned_data.get('file')
            # with open(file, 'r', encoding="utf-8", errors='ignore') as fp:
            #    default_storage.save(f'photos/{file.name}', fp)

            handle_import(request, f'media/import-listing/{file.name}', listing_type=request.POST.get('listing_type'))

            return JsonResponse({})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)}, status=400)
    return JsonResponse({})


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingHistory, ListingHistoryAdmin)
