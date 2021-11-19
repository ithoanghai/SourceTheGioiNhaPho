from django.contrib import admin
from django.db.models import Q
from .models import Customer
from ..realtors.models import Realtor


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'financial_range', 'district', 'status', 'classify', 'user')
    list_display_links = ('name', 'phone',)
    search_fields = ('name', 'phone', 'email', 'address', 'financial_range', 'district', 'status', 'classify')
    list_per_page = 100
    change_form_template = 'custom_change_form.html'

    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = super().get_queryset(request)
            return queryset
        else:
            queryset_list = Customer.objects.order_by('-hire_date')
            query = Q(realtor__user=request.user.id)
            query = query | Q(user=request.user)
            queryset_list = queryset_list.filter(query)
            return queryset_list

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(CustomerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user'
        }
        if request.user.is_superuser:
            realtor = Realtor.objects.filter(user=request.user)
            form.base_fields['realtor'].initial = realtor

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj)
        user = request.user
        to_exclude = []
        if not user.is_superuser:
            to_exclude.append(("realtor", "user"))
        try:
            return list(excluded) + to_exclude
        except TypeError:
            return to_exclude


admin.site.register(Customer, CustomerAdmin)
