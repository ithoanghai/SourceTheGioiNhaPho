from django.contrib import admin
from django.urls import path

from . import views

admin.autodiscover()

urlpatterns = [
    path('contact', views.contact, name='post_contact'),
    path('', views.index, name='transaction'),
    path('<int:transaction_id>', views.transaction, name='transaction_detail'),
    path('request_quote', views.request_quote, name='request_quote'),


]
