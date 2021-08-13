from django.contrib import admin

from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'realtor_name', 'hire_date')
    list_display_links = ('realtor_name',)
    search_fields = ('realtor_name',)
    list_per_page = 25

    def realtor_name(self, obj: Realtor):
        return obj.user.name


admin.site.register(Realtor, RealtorAdmin)
