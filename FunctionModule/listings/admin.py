import fractions

from django.contrib import admin
from django.contrib.admin import FieldListFilter, BooleanFieldListFilter, DateFieldListFilter
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, JsonResponse

from FunctionModule.listings.import_csv import handle_import, logger
from .filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter, IsWithinRangeFilter
from .forms import ListingAdminForm, ImportListingForm, ImageForm, ImageFormSet
from .models import Listing, ListingImage, ListingVideo, ContractImage
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
    list_display = ('address', 'district','area', 'floors', 'width', 'price', 'average_price', 'road_type', 'house_type', 'code', 'status', 'is_published')
    list_display_links = ('code','district',)
    list_filter = (
        ('status', ChoiceDropdownFilter),
        ('house_type', ChoiceDropdownFilter),
        ('floors', ChoiceDropdownFilter),
        ('road_type', ChoiceDropdownFilter),
        ('registration_type', ChoiceDropdownFilter),
        ('realtor', RelatedDropdownFilter),
        ('transaction_type', ChoiceDropdownFilter),
        ('list_date', DateFieldListFilter),
        ('is_published', BooleanFieldListFilter),
    )
    list_editable = ('address',)
    search_fields = ('title', 'code', 'address','area', 'price','house_type', 'road_type', 'urban_area', 'street','ward', 'district','state', 'list_date',)
    list_per_page = 100
    inlines = [ListingPhotoAdmin, ListingVideoAdmin, ContractPhotoAdmin]
    actions = ['make_published', 'unpublished']
    form = ListingAdminForm
    ordering = ('-list_date','price', 'average_price', 'road_type','-area', 'district')

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/listing.js', 'admin/js/filepond-4.28.2.min.js',
              'admin/js/micromodal-0.4.6.min.js')
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css', 'admin/css/filepond.min.css')
        }

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(ListingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user'
        }
        if request.user.is_superuser:
            realtor = Realtor.objects.filter(user=request.user)
            form.base_fields['realtor'].initial = realtor
        else:
            self.exclude = ("realtor",)

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = super().get_queryset(request)
            return queryset
        else:
            queryset_list = Listing.objects.order_by('-list_date')
            query = Q(realtor__user=request.user.id)
            query = query | Q(user=request.user)
            queryset_list = queryset_list.filter(query)
            return queryset_list

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj)
        user = request.user
        to_exclude = []
        if obj is None:
            to_exclude += []
        else:
            if not user.is_superuser:
                to_exclude.append(('realtor', 'user'))
                if obj.realtor.user != user.id:
                    to_exclude.append('address')
        try:
            return list(excluded) + to_exclude
        except TypeError:
            return to_exclude

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Đã đổi trạng thái cho {updated} căn')

    def unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Đã đổi trạng thái cho {updated} căn')

@admin.site.register_view('listings/listing/import-listing')
def import_csv_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = ImportListingForm(request.POST, request.FILES)
        if form.is_valid():
            file: UploadedFile = form.cleaned_data.get('file')
            #with open(file, 'r', encoding="utf-8", errors='ignore') as fp:
            #    default_storage.save(f'photos/{file.name}', fp)

            handle_import(f'media/import-listing/{file.name}', listing_type=request.POST.get('listing_type'))

            return JsonResponse({})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)}, status=400)
    return JsonResponse({})


admin.site.register(Listing, ListingAdmin)
