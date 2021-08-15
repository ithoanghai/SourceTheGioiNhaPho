from django.contrib import admin
from django.urls import path

from . import views

admin.autodiscover()

urlpatterns = [
    path('contact', views.contact, name='post_contact'),
    path('request_quote', views.request_quote, name='request_quote'),

    path('transactionsAPIView/', views.transactionsAPIView.as_view(), name='transactionsAPIView'),
    path('transactionsAPI1', views.transactionsAPIViewWay1)
]
