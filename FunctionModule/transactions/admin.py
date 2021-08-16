from django.contrib import admin

from .forms import TransactionAdminForm
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'message', 'listing', 'user', 'date', 'trantype', 'status')
  list_display_links = ('id', 'message',)
  search_fields = ('listing', 'message', 'user',)
  list_per_page = 25
  form = TransactionAdminForm


admin.site.register(Transaction, TransactionAdmin)
