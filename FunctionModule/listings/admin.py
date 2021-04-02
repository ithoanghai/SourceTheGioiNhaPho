from django.contrib import admin

from .forms import ListingAdminForm
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
        js = ('admin/js/text_money.js', 'admin/js/address_select.js')
        css = {
            'all': ('admin/css/listing.css',)
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


admin.site.register(Listing, ListingAdmin)
