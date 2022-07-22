import fractions

from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django import forms
from django.http import HttpRequest, JsonResponse
from django_filters import RangeFilter

from FunctionModule.listings.import_csv import handle_import, logger
from . import Status
from .filters import RangeFilter
from .forms import ListingAdminForm, ImportListingForm, ImageForm, ImageFormSet
from .models import Listing, ListingImage, ListingVideo, ContractImage, ListingHistory
from .choices import district_default_choices
from ..filters import DropdownFilter, DateFieldFilter, BooleanFieldFilter
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

    list_display = ('address', 'area', 'floors', 'width', 'price', 'average_price', 'road_type', 'house_type', 'district','list_date')
    list_display_links = ('address',)
    list_filter = (
        ('status', DropdownFilter),
        ('house_type', DropdownFilter),
        ('transaction_type', DropdownFilter),
        ('road_type', DropdownFilter),
        ('floors', DropdownFilter),
        ('registration_type', DropdownFilter),
        ('list_date', DateFieldFilter),
        ('is_published', BooleanFieldFilter),
        ('is_advertising', BooleanFieldFilter),
        #AreaFilter,
    )
    #advanced_filter_fields = ('status', ('house_type', 'road_type'))
    list_editable = ()
    search_fields = ('id', 'title', 'code', 'address', 'area', 'price', 'house_type', 'road_type', 'urban_area',
                     'street', 'ward', 'district', 'state', 'list_date',)
    list_per_page = 200
    inlines = [ListingPhotoAdmin, ListingVideoAdmin, ContractPhotoAdmin]
    actions = ['make_published', 'unpublished', 'sold']
    form = ListingAdminForm
    ordering = ('-list_date',)
    #delete_selected.short_description = 'Xóa bất động sản đã chọn trong %(verbose_name_plural)'

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

    #@admin.actions(short_description='Đăng bán công khai')
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Chuyển sang chế độ đăng công khai cho {updated} căn')

    #@admin.actions(short_description='Không đăng bán')
    def unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Đã đổi trạng thái riêng tư cho {updated} căn')

    #@admin.actions(short_description='Chuyển sang trạng thái đã bán')
    def sold(self, request, queryset):
        updated = queryset.update(status=Status.SOLD)
        self.message_user(request, f'Đã đổi trạng thái đã bán cho {updated} căn')


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
    list_filter = ('list_date', 'listing', )
    list_filter = (
        ('floors', DropdownFilter),
        ('list_date', DateFieldFilter),
    )
    list_editable = ()
    search_fields = ('id','listing', 'area', 'price', 'list_date',)
    list_per_page = 200
    inlines = []
    actions = []
    form = ListingAdminForm
    ordering = ('-list_date',)
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
            queryset_list = Listing.objects.order_by('-list_date')
            query = Q(realtor__user=request.user.id)
            query = query | Q(user=request.user)
            queryset_list = queryset_list.filter(query)
            return queryset_list


@admin.site.register_view('listings/listing/import-export')
def import_csv_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = ImportListingForm(request.POST or None, request.FILES)
        if form.is_valid():
            #file = request.FILES.get('file')
            #filename = file._get_name()
            #fd = open('%s/import-export/%Y%m%d/%s' % (MEDIA_ROOT, str(filename)), 'wb')
            #fd = open(file, 'r', encoding="utf-8", errors='ignore')
            #for chunk in file.chunks():
            #    fd.write(chunk)
            #fd.close()
            file: UploadedFile = form.cleaned_data.get('file')
            #with open(file, 'r', encoding="utf-8", errors='ignore') as fp:
            #   default_storage.save(BASE_DIR, f'media/import-export/{file.name}', fp)

            handle_import(request, f'media/import-export/{file.name}', listing_type=request.POST.get('listing_type'))

            return JsonResponse({})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)}, status=400)
    return JsonResponse({})


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingHistory, ListingHistoryAdmin)
