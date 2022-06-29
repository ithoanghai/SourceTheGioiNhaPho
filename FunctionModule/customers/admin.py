from django.contrib import admin
from django.db.models import Q
from .forms import CustomerAdminForm
from .models import Customer
from ..filters import DropdownFilter, DateFieldFilter
from ..realtors.models import Realtor


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN KHÁCH HÀNG', {'fields': (
            ('custormer_type','status'), ('name', 'phone','email'),
            ('address', 'financial_range'),
            ('contact_from','district',), 'descriptions', 'listing_watched', )}),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': (('hire_date','last_interaction'),)}),
        ('NHẬN ĐỊNH CỦA CHUYÊN VIÊN', {
            'fields': (('transactionStatus', 'classify'),)
        }),
    )
    list_display = ('id', 'name', 'phone', 'financial_range', 'district', 'request', 'custormer_type', 'classify', )
    list_display_links = ('name', 'phone',)
    search_fields = ('name', 'phone', 'email', 'address', 'financial_range', 'request', 'descriptions', 'district', 'custormer_type', 'status', 'classify')
    list_per_page = 100
    ordering = ('financial_range', 'district', 'name', 'hire_date')
    list_filter = ('transactionStatus', 'custormer_type', 'classify', 'status', 'hire_date',)
    list_filter = (
        ('transactionStatus', DropdownFilter),
        ('custormer_type', DropdownFilter),
        ('classify', DropdownFilter),
        ('status', DropdownFilter),
        ('hire_date', DateFieldFilter),
    )
    form = CustomerAdminForm

    def get_queryset(self, request):
        #if request.user.is_superuser:
        #    queryset = super().get_queryset(request)
        #    return queryset
        #else:
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
