from rest_framework.authtoken.views import obtain_auth_token 
from django.contrib import admin
from django.urls import path, include

from . import views

admin.autodiscover()

urlpatterns = [
    path('search', views.search, name='realtor_search'),

]
