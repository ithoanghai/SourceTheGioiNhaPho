from django.contrib import admin
from django.urls import path

from . import views

admin.autodiscover()

urlpatterns = [
    path('', views.index, name='customer'),
    path('<int:customer_id>', views.customer, name='customer_detail')
]
