from django.contrib import admin

from .forms import TransactionAdminForm
from .models import Transaction, TransactionHistory


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'trantype', 'message', 'location', 'request_price', 'house_type', 'listing', 'customer', 'date', 'status')
  list_display_links = ('id', 'message',)
  search_fields = ('listing', 'message', 'customer',)
  list_per_page = 100
  form = TransactionAdminForm


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionHistory)
