from django.contrib import admin

from FunctionModule import admin_site
from django.core.files.uploadedfile import UploadedFile
from django import forms
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.db.models import Q
from django.utils.translation import gettext as _, gettext_lazy

from FunctionModule.listings.import_csv import handle_import, logger
from . import Status
from .forms import ListingAdminForm, ImportListingForm, ImageForm, ImageFormSet, ContractImageForm, ContractImageFormSet
from .models import Listing, ListingImage, ListingVideo, ContractImage, ListingHistory
from .choices import district_default_choices, Exhaustive
from ..admin_site.filters import DateFieldListFilter, BooleanFieldListFilter, ChoicesFieldListFilter, RangeNumericFilter
from ..realtors.models import Realtor
from ..transactions.models import Transaction


class ListingPhotoAdmin(admin_site.TabularInline):
    model = ListingImage
    verbose_name = "HÌNH ẢNH CHỤP BĐS"
    form = ImageForm
    formset = ImageFormSet

    max_num = 25
    extra = 0


class ContractPhotoAdmin(admin_site.TabularInline):
    model = ContractImage
    verbose_name = "ẢNH HỢP ĐỒNG TRÍCH THƯỞNG & PHIẾU KHẢO SÁT BĐS"
    form = ContractImageForm
    formset = ContractImageFormSet

    max_num = 10
    extra = 0


class ListingVideoAdmin(admin_site.TabularInline):
    model = ListingVideo
    extra = 0
    verbose_name = "VIDEO QUAY BĐS"


class ListingHistoryInline(admin_site.TabularInline):
    model = ListingHistory
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created', 'area','floors', 'price', 'extra_data', 'warehouse', )


class TransactionInline(admin_site.TabularInline):
    model = Transaction
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'status', 'trantype', 'request_price', 'customer', 'realtor',)
    can_delete = False
    readonly_fields = ('date', 'realtor', 'customer',)


class ListingAdmin(admin_site.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN GIAO DỊCH', {'fields': (
            ('transaction_type', 'house_type', 'is_exclusive', 'is_verified', ),)}),
        ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
            ('title', 'code'), ('description', 'extra_data'),
            ('area', 'floors', 'width'), ('price', 'registration_type', 'road_type'),
        )}),
        ('TRẠNG THÁI KHẢO SÁT', {'fields': (
            ('exhaustive', 'liquidity_classification'), ('expert_comments',))}),
        ('ĐỊA CHỈ & VỊ TRÍ BĐS', {'fields': (
            ('state', 'district', 'ward'), ('street', 'address', 'location'))}),
        ('TRẠNG THÁI ĐĂNG TIN', {
            'fields': (('status', 'date_created', 'date_update'), ('is_published', 'priority'),)}),
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
        ('area', RangeNumericFilter),
        ('floors', RangeNumericFilter),
        ('width', RangeNumericFilter),
        ('price', RangeNumericFilter),
        ('average_price', RangeNumericFilter),
        ('bedrooms', RangeNumericFilter),
        ('priority', RangeNumericFilter),
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
    #delete_selected.short_description = 'Xóa bất động sản đã chọn trong %(verbose_name_plural)'

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

    #@admin.actions(short_description='Đăng bán công khai')
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Chuyển sang chế độ đăng công khai cho {updated} bất động sản')

    #@admin.actions(short_description='Không đăng bán')
    def unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Đã đổi trạng thái riêng tư cho {updated} bất động sản')

    #@admin.actions(short_description='Chuyển sang trạng thái đã bán')
    def sold(self, request, queryset):
        updated = queryset.update(status=Status.SOLD)
        self.message_user(request, f'Đã đổi trạng thái đã bán cho {updated} bất động sản')

    # @admin.actions(short_description='Chuyển sang trạng thái chuẩn bị đi khảo sát')
    def exhaustive(self, request, queryset):
        updated = queryset.update(exhaustive=Exhaustive.PREPARE)
        self.message_user(request, f'Đã lên lịch khảo sát {updated} bất động sản')

    make_published.short_description = _("Đăng công khai")
    unpublished.short_description = _("Hủy đăng công khai")
    sold.short_description = _("Đã bán/cho thuê")
    exhaustive.short_description = _("Lên lịch đi khảo sát")


class ListingHistoryAdmin(admin_site.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
            ('listing','address'),
            'extra_data',
            ('area', 'floors', 'width'), ('price', 'bedrooms', 'bathrooms'),
            ('warehouse', 'date_created'), ('reward_person', 'reward_person_mobile'),
        )}),
    )

    list_display = ('listing', 'area', 'floors', 'width', 'price', 'warehouse', 'date_created',)
    list_display_links = ('listing',)
    list_filter = (
        ('area', RangeNumericFilter),
        ('floors', RangeNumericFilter),
        ('width', RangeNumericFilter),
        ('price', RangeNumericFilter),
        ('bedrooms', RangeNumericFilter),
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


@admin_site.site.register_view('listings/listing/import-export')
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


admin_site.site.register(Listing, ListingAdmin)
admin_site.site.register(ListingHistory, ListingHistoryAdmin)
