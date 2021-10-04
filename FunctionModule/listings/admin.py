from django.contrib import admin
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, JsonResponse

from FunctionModule.listings.import_csv import handle_import
from .forms import ListingAdminForm, ImportListingForm, ImageForm, ImageFormSet
from .models import Listing, ListingImage, ListingVideo, ContractImage
from ..realtors.models import Realtor


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
    list_display = ('code', 'title', 'price', 'location_name', 'list_date', 'realtor_name', 'is_published')
    list_display_links = ('code',)
    list_filter = ('price', 'list_date',)
    list_editable = ('title',)
    search_fields = ('title', 'code', 'address', 'price', 'street', 'district',)
    list_per_page = 50
    inlines = [ListingPhotoAdmin, ListingVideoAdmin, ContractPhotoAdmin]
    form = ListingAdminForm

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/listing.js', 'admin/js/filepond-4.28.2.min.js',
              'admin/js/micromodal-0.4.6.min.js')
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css', 'admin/css/filepond.min.css')
        }

    def realtor_name(self, obj: Realtor):
        return obj.realtor.user.name

    def location_name(self, obj: Listing):
        return f'%s - %s' % (obj.ward_name() , obj.district_name())

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(realtor__user=request.user.id)

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj)
        user = request.user
        to_exclude = ['list_date']
        if obj is None:
            to_exclude += []
        else:
            if not user.is_superuser:
                if obj.realtor.user != user.id:
                    to_exclude.append('address')
        try:
            return list(excluded) + to_exclude
        except TypeError:
            return to_exclude


@admin.site.register_view('listings/listing/import-listing')
def import_csv_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = ImportListingForm(request.POST, request.FILES)
        if form.is_valid():
            file: UploadedFile = form.cleaned_data.get('file')
            #with open(file, 'r', encoding="utf-8", errors='ignore') as fp:
            #    default_storage.save(f'photos/{file.name}', fp)

            handle_import(f'media/import-listing/{file.name}')

            return JsonResponse({})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)}, status=400)
    return JsonResponse({})


admin.site.register(Listing, ListingAdmin)
