from FunctionModule import admin_site

from .forms import TransactionAdminForm, TransactionHistoryAdminForm
from .models import Transaction, TransactionHistory
from FunctionModule.admin_site.filters import ChoicesFieldListFilter, RangeNumericFilter
from ..admin_site import DateFieldListFilter


class TransactionAdmin(admin_site.ModelAdmin):
  fieldsets = (
    ('THÔNG TIN CHUYÊN VIÊN', {
      'classes': ('wide',),
      'fields': (('realtor', 'user'),)}),
    ('THÔNG TIN GIAO DỊCH', {'fields': (
      ('trantype', 'status','date'),)}),
    ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
      ('listing', 'house_type'),)}),
    ('THÔNG TIN KHÁCH HÀNG', {'fields': (
      ('customer', 'caring_area', 'request_price'), ('message', 'comment'),)}),
  )

  list_display = ('id', 'trantype', 'message', 'caring_area', 'request_price', 'house_type', 'listing', 'customer', 'user', 'date', 'status')
  list_display_links = ('id', 'trantype', 'message',)
  ordering = ('-date',)
  search_fields = ('message','caring_area', 'request_price','comment')
  autocomplete_fields = ['listing', 'customer', 'user', 'realtor']
  list_filter = (
    ('trantype', ChoicesFieldListFilter),
    ('house_type', ChoicesFieldListFilter),
    ('status', ChoicesFieldListFilter),
    ('date', DateFieldListFilter),
    ('request_price', RangeNumericFilter),
  )
  list_per_page = 100
  form = TransactionAdminForm

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


class TransactionHistoryAdmin(admin_site.ModelAdmin):
  fieldsets = (
    ('THÔNG TIN GIAO DỊCH', {'fields': (
      'transaction', ('status','reason'),)}),
    ('NỘI DUNG', {'fields': (
      'comment',)}),
    ('CHUYÊN VIÊN & THỜI GIAN THỰC HIỆN', {'fields': (
      'realtor', 'date',)}),
  )

  list_display = ('id', 'transaction', 'status', 'comment', 'reason','realtor', 'date')
  list_display_links = ('id', 'transaction', 'comment',)
  search_fields = ('transaction', 'comment', 'realtor',)
  list_per_page = 100
  form = TransactionHistoryAdminForm


admin_site.site.register(Transaction, TransactionAdmin)
#admin.site.register(TransactionHistory, TransactionHistoryAdmin)
