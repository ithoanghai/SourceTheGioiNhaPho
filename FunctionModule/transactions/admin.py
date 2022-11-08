from django.forms import Textarea
from django.http import HttpRequest, HttpResponse

from FunctionModule import admin_site
from FunctionModule.admin_site.filters import ChoicesFieldListFilter, RangeNumericFilter
from .forms import TransactionAdminForm, TransactionHistoryAdminForm
from .models import Transaction, TransactionHistory
from ..admin_site import DateFieldListFilter
from ..realtors.models import Realtor


class TransactionHistoryInline(admin_site.TabularInline):
    model = TransactionHistory
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'transaction', 'status', 'reason', 'comment',  'realtor', )
    readonly_fields = ('date', 'realtor',)
    can_delete = False


class TransactionAdmin(admin_site.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': (('realtor', 'user'),)}),
        ('THÔNG TIN GIAO DỊCH', {'fields': (
            ('trantype', 'status', 'date'),)}),
        ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
            ('listing', 'house_type'),)}),
        ('THÔNG TIN KHÁCH HÀNG', {'fields': (
            ('customer', 'caring_area', 'request_price'), ('message', 'comment'),)}),
    )

    list_display = (
    'id', 'trantype', 'message', 'caring_area', 'request_price', 'house_type', 'listing', 'customer', 'created_date',
    'status')
    list_display_links = ('id', 'trantype', 'message',)
    ordering = ('-date',)
    search_fields = ('message', 'caring_area', 'request_price', 'comment')
    autocomplete_fields = ['listing', 'customer', 'user', 'realtor']
    readonly_fields = ('trantype', 'message', 'comment', 'caring_area', 'request_price', 'house_type', 'listing', 'customer', 'date',)
    list_filter = (
        ('trantype', ChoicesFieldListFilter),
        ('house_type', ChoicesFieldListFilter),
        ('status', ChoicesFieldListFilter),
        ('date', DateFieldListFilter),
        ('request_price', RangeNumericFilter),
    )
    list_per_page = 100
    form = TransactionAdminForm
    inlines = [TransactionHistoryInline, ]
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    actions_on_top = False
    actions_on_bottom = False
    actions_selection_counter = False

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(TransactionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user',
        }
        if request.user.is_superuser:
            form.base_fields['user'].disabled = True
        elif request.user.is_staff:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        else:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        return form

    def changeform_view(
            self,
            request: HttpRequest,
            object_id: int = None,
            form_url: str = '',
            extra_context: dict = None
    ) -> HttpResponse:

        extra_context = extra_context or {}
        extra_context.update({
            'transaction_interact_history': True,
        })
        return super().changeform_view(request, object_id, extra_context=extra_context)


class TransactionHistoryAdmin(admin_site.ModelAdmin):
    fieldsets = (
        ('THÔNG TIN GIAO DỊCH', {'fields': (
            'transaction', ('status', 'reason'),)}),
        ('NỘI DUNG', {'fields': (
            'comment',)}),
        ('CHUYÊN VIÊN & THỜI GIAN THỰC HIỆN', {'fields': (
            'realtor', 'date',)}),
    )

    list_display = ('id', 'transaction', 'status', 'comment', 'reason', 'realtor', 'answer_date')
    list_display_links = ('id', 'transaction', 'comment',)
    search_fields = ('transaction', 'comment', 'realtor',)
    autocomplete_fields = ['transaction', 'realtor']
    list_per_page = 100
    form = TransactionHistoryAdminForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(TransactionHistoryAdmin, self).get_form(request, obj, **kwargs)
        realtor_list = Realtor.objects.filter(user=request.user)
        if realtor_list is not None:
            form.base_fields['realtor'].initial = realtor_list.first()
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'realtor',
        }
        if request.user.is_superuser:
            form.base_fields['realtor'].disabled = False
        elif request.user.is_staff:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        else:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        return form


admin_site.site.register(Transaction, TransactionAdmin)
admin_site.site.register(TransactionHistory, TransactionHistoryAdmin)
