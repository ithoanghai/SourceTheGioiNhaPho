from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'listing', 'user', 'date', 'status')
  list_display_links = ('id', 'listing', 'user',)
  search_fields = ('listing', 'user',)
  list_per_page = 25

admin.site.register(Transaction)
