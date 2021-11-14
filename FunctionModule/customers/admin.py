from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'hire_date')
    list_display_links = ('name',)
    search_fields = ('name', 'phone', 'email', 'address')
    list_per_page = 100


admin.site.register(Customer, CustomerAdmin)
