from rest_framework.authtoken.views import obtain_auth_token 
from FunctionModule import admin_site
from django.urls import path, include
from django.conf.urls import url

from . import views
from .views import ListingDetailJSONView

admin_site.autodiscover()

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:listing_id>', views.listing,  name='listing_detail'),
    #url(r'^(?P<pk>\d+)/$', ListingDetailJSONView.as_view(), name='listing_detail'),
    path('my_listing', views.my_listing, name='my_listing'),

    path('my_listing_post', views.my_listing_post, name='my_listing_post'),
    path('post_listing', views.post_listing, name='post_listings'),

    path('search', views.search, name='listing_search'),

    path('sell_lease_with_us', views.sell_lease_with_us, name='sell_lease_with_us'),
    path('buy_with_us', views.buy_with_us, name='buy_with_us'),
    path('rent_with_us', views.rent_with_us, name='rent_with_us'),

    path('ListingsAPIView/', views.ListingsAPIView.as_view(), name='ListingsAPIView'),
    path('listingsAPI', views.listing_api_view),
    path('ListingAPIAllView', views.ListingAPIAllView.as_view()),
    path('listings-api-token-auth/', obtain_auth_token, name='listings_api_token_auth'),

    path('listinghistory/add/', views.listinghistoryadd, name='history_add'),

]
