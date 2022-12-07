from rest_framework.authtoken.views import obtain_auth_token 
from FunctionModule import admin_site
from django.urls import path, include

from . import views

admin_site.autodiscover()

urlpatterns = [
    path('search', views.search, name='realtor_search'),

]
