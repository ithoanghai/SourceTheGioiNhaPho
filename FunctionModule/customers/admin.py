from FunctionModule import admin_site
from django.db.models import Q
from .forms import CustomerAdminForm
from .models import Customer
from FunctionModule.admin_site.filters import ChoicesFieldListFilter, RangeNumericFilter
from ..admin_site import DateFieldListFilter
from ..realtors.models import Realtor


class CustomerAdmin(admin_site.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN KHÁCH HÀNG', {'fields': (
            ('transactionStatus', 'custormer_type'), ('house_type', 'status'), ('name', 'phone','email'),
            ('address', 'financial_range','district'),
            ('descriptions', 'listing_watched'), )}),
        ('GIỚI THIỆU & LIÊN HỆ', {'fields': (('contact_from'),)}),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': (('hire_date','last_interaction'),)}),
        ('NHẬN ĐỊNH CỦA CHUYÊN VIÊN', {
            'fields': (('classify'),)
        }),
    )
    list_display = ('id', 'name', 'phone', 'financial_range', 'district', 'descriptions', 'custormer_type', 'transactionStatus', 'classify', )
    list_display_links = ('name', 'phone',)
    search_fields = ('name', 'phone', 'email', 'address', 'financial_range', 'district', 'descriptions', 'district', 'contact_from', 'listing_watched', 'classify')
    autocomplete_fields = ['user', 'realtor']
    list_per_page = 100
    ordering = ('-hire_date', 'financial_range', 'district', 'name',)
    list_filter = ('transactionStatus', 'custormer_type', 'classify', 'status', 'hire_date',)
    list_filter = (
        ('transactionStatus', ChoicesFieldListFilter),
        ('custormer_type', ChoicesFieldListFilter),
        ('house_type', ChoicesFieldListFilter),
        ('classify', ChoicesFieldListFilter),
        ('status', ChoicesFieldListFilter),
        ('hire_date', DateFieldListFilter),
        ('financial_range', RangeNumericFilter),
    )
    form = CustomerAdminForm

    def get_queryset(self, request):
        #if request.user.is_superuser:
        #    queryset = super().get_queryset(request)
        #    return queryset
        #else:
        queryset_list = Customer.objects.order_by('-hire_date')
        query = Q(realtor__user=request.user.id)
        query = query | Q(user=request.user) | Q(realtor__user=request.user)
        queryset_list = queryset_list.filter(query)
        return queryset_list

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(CustomerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user'
        }

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


admin_site.site.register(Customer, CustomerAdmin)
