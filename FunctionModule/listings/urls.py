from rest_framework.authtoken.views import obtain_auth_token 
from django.contrib import admin
from django.urls import path, include
from ajax_select import urls as ajax_select_urls

from . import views
from .views import ListingDetailJSONView

admin.autodiscover()

urlpatterns = [
    path('', views.index),
    path('<int:listing_id>', views.listing,  name='listing_detail'),
    #re_path(r'^(?P<pk>\d+)/$', ListingDetailJSONView.as_view(), name='listing_detail'),
    path('mylisting', views.mylisting, name='mylisting'),

    path('mylistingpost', views.mylistingpost, name='mylistingpost'),
    path('postlisting', views.ListingCreateView.as_view(), name='postlistings'),

    path('search', views.search, name='listing_search'),

    path('sellleaseus', views.sellleaseus, name='sellleaseus'),
    path('buywithus', views.buywithus, name='buywithus'),
    path('rentwithus', views.rentwithus, name='rentwithus'),

    path('ListingsAPIView/', views.ListingsAPIView.as_view(), name='ListingsAPIView'),
    path('listingsAPI', views.listing_api_view),
    path('ListingsAPIView/', views.ListingsAPIView.as_view(), name='ListingsAPIView'),
    path('ListingAPIAllView', views.ListingAPIAllView.as_view()),
    path('listings-api-token-auth/', obtain_auth_token, name='listings_api_token_auth'),

    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),

]
