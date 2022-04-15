from django.contrib import admin

from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'hire_date')
    list_display_links = ('user',)
    search_fields = ('id', 'hire_date')
    list_per_page = 200
    ordering = ('user', 'hire_date')

admin.site.register(Realtor, RealtorAdmin)
