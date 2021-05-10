from django.contrib import admin
from django.urls import path

from . import views

admin.autodiscover()

urlpatterns = [
    path('', views.index, name='transactions'),
    path('<int:transaction_id>', views.transaction, name='transaction'),
    path('search', views.search, name='search'),
    path('detail', views.detail, name='detail'),

    path('transactionsAPIView/', views.transactionsAPIView.as_view(), name='transactionsAPIView'),
    path('transactionsAPI1', views.transactionsAPIViewWay1)
]
