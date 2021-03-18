from django.contrib import admin

from .models import Listing, ListingImage


class ListingPhotoAdmin(admin.TabularInline):
    model = ListingImage


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
    list_display_links = ('id', 'title')
    list_filter = ('realtor',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
    list_per_page = 25
    inlines = [ListingPhotoAdmin]

    class Media:
        js = ('js/admin/text_money.js',)
        css = {
            'all': ('css/admin/listing.css',)
        }


admin.site.register(Listing, ListingAdmin)
