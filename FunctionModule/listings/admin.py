from django.contrib import admin
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, JsonResponse

from FunctionModule.listings.import_csv import handle_import
from .forms import ListingAdminForm, ImportListingForm
from .models import Listing, ListingImage, ListingVideo


class ListingPhotoAdmin(admin.TabularInline):
    model = ListingImage


class ListingVideoAdmin(admin.TabularInline):
    model = ListingVideo
    extra = 1


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'is_published', 'price', 'list_date', 'realtor')
    list_display_links = ('id', 'title')
    list_filter = ('realtor',)
    list_editable = ('is_published', 'code')
    search_fields = ('title', 'code', 'address', 'price')
    list_per_page = 25
    inlines = [ListingPhotoAdmin, ListingVideoAdmin]
    form = ListingAdminForm

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/listing.js',)
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css',)
        }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=request.user.id)

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj)
        to_exclude = ['list_date']
        if obj is None:
            to_exclude += []
        else:
            pass
        try:
            return list(excluded) + to_exclude
        except TypeError:
            return to_exclude


@admin.site.register_view('listings/listing/import-listing')
def my_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = ImportListingForm(request.POST, request.FILES)
        if form.is_valid():
            file: UploadedFile = form.cleaned_data.get('file')
            with file.open() as fp:
                default_storage.save(f'import-listing/{file.name}', fp)

            handle_import(f'media/import-listing/{file.name}')

            return JsonResponse({})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)}, status=400)
    return JsonResponse({})


admin.site.register(Listing, ListingAdmin)
