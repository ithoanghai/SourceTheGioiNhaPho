from django.contrib import admin

from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'realtor_name', 'hire_date')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_per_page = 25

    def realtor_name(self, obj: Realtor):
        return obj.user.name


admin.site.register(Realtor, RealtorAdmin)
