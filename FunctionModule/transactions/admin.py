from django.contrib import admin

from .forms import TransactionAdminForm, TransactionHistoryAdminForm
from .models import Transaction, TransactionHistory


class TransactionAdmin(admin.ModelAdmin):
  fieldsets = (
    ('THÔNG TIN CHUYÊN VIÊN', {
      'classes': ('wide',),
      'fields': ('realtor',)}),
    ('THÔNG TIN GIAO DỊCH', {'fields': (
      ('trantype', 'status','date'),)}),
    ('THÔNG TIN BẤT ĐỘNG SẢN', {'fields': (
      ('listing', 'house_type'),)}),
    ('THÔNG TIN KHÁCH HÀNG', {'fields': (
      ('customer', 'caring_area', 'request_price'), ('message', 'comment'),)}),
  )

  list_display = ('id', 'trantype', 'message', 'caring_area', 'request_price', 'house_type', 'listing', 'customer', 'date', 'status')
  list_display_links = ('id', 'trantype', 'message',)
  search_fields = ('listing', 'message', 'customer',)
  list_per_page = 100
  form = TransactionAdminForm


class TransactionHistoryAdmin(admin.ModelAdmin):
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


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
