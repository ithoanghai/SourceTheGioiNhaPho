from django.contrib import admin

from .forms import TransactionAdminForm
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'trantype', 'message', 'location', 'request_price', 'house_type', 'listing', 'user', 'date', 'status')
  list_display_links = ('id', 'message',)
  search_fields = ('listing', 'message', 'user',)
  list_per_page = 25
  form = TransactionAdminForm


admin.site.register(Transaction, TransactionAdmin)
