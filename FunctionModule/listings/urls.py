from rest_framework.authtoken.views import obtain_auth_token 
from django.contrib import admin
from django.urls import path

from . import views

admin.autodiscover()

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),

    path('search', views.search, name='search'),

    path('detail', views.detail, name='detail'),
    path('sellwithus', views.sell_with_us, name='sell_with_us'),
    path('buywithus', views.buy_with_us, name='buy_with_us'),
    path('rentwithus', views.rent_with_us, name='rent_with_us'),

    path('listingsAPIView/', views.listingsAPIView.as_view(), name='listingsAPIView'),
    path('listingsAPI', views.listingsAPI),
    path('listingAPIall', views.listingAPIall.as_view()),
    path('listings-api-token-auth/', obtain_auth_token, name='listings_api_token_auth'),
]
