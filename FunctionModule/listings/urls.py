from rest_framework.authtoken.views import obtain_auth_token 
from FunctionModule import admin_site
from django.urls import path, include
from django.conf.urls import url
from ajax_select import urls as ajax_select_urls

from . import views
from .views import ListingDetailJSONView

admin_site.autodiscover()

urlpatterns = [
    path('', views.index),
    path('<int:listing_id>', views.listing,  name='listing_detail'),
    #url(r'^(?P<pk>\d+)/$', ListingDetailJSONView.as_view(), name='listing_detail'),
    path('myListing', views.myListing, name='myListing'),

    path('mylistingpost', views.mylistingpost, name='mylistingpost'),
    path('postListing', views.ListingCreateView.as_view(), name='postListings'),

    path('search', views.search, name='listing_search'),

    path('sellleaseus', views.sellleaseus, name='sellleaseus'),
    path('buywithus', views.buywithus, name='buywithus'),
    path('rentwithus', views.rentwithus, name='rentwithus'),

    path('ListingsAPIView/', views.ListingsAPIView.as_view(), name='ListingsAPIView'),
    path('listingsAPI', views.listing_api_view),
    path('ListingAPIAllView', views.ListingAPIAllView.as_view()),
    path('listings-api-token-auth/', obtain_auth_token, name='listings_api_token_auth'),

    path('listinghistory/add/', views.listinghistoryadd, name='history_add'),

    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),

]
