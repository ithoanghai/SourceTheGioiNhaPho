from django.contrib import admin

from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hire_date')
    list_display_links = ('user',)
    search_fields = ('id', 'hire_date')
    list_per_page = 100


admin.site.register(Realtor, RealtorAdmin)
