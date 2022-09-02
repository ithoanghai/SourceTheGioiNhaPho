from FunctionModule import admin_site
from django.urls import path

from . import views

admin_site.autodiscover()

urlpatterns = [
    path('', views.index, name='customer'),
    path('<int:customer_id>', views.customer, name='customer_detail')
]
