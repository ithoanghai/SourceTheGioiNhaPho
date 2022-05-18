from rest_framework.authtoken.views import obtain_auth_token 
from django.contrib import admin
from django.urls import path, include

from . import views

admin.autodiscover()

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing_detail'),
    path('post_listing', views.post_listing, name='post_listings'),

    path('search', views.search, name='listing_search'),
    path('search_simple', views.search_simple, name='listing_search_simple'),

    path('sell_lease_with_us', views.sell_lease_with_us, name='sell_lease_with_us'),
    path('buy_with_us', views.buy_with_us, name='buy_with_us'),
    path('rent_with_us', views.rent_with_us, name='rent_with_us'),

    path('ListingsAPIView/', views.ListingsAPIView.as_view(), name='ListingsAPIView'),
    path('listingsAPI', views.listing_api_view),
    path('ListingAPIAllView', views.ListingAPIAllView.as_view()),
    path('listings-api-token-auth/', obtain_auth_token, name='listings_api_token_auth'),

    #path('advanced_filters/', include('advanced_filters.urls'))
]
