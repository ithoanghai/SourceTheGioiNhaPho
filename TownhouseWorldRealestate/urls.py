import debug_toolbar
from importlib import import_module
from django.urls import re_path, path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from FunctionModule.pages.sitemaps import Listing_Sitemap, Static_Sitemap, Blog_Sitemap
from FunctionModule.pages.views import handler404, handler500, pages
from TownhouseWorldRealestate import settings

#admin.autodiscover()
admin.site.site_header = 'Quản trị hệ thống thế giới nhà phố'

sitemaps = {
    'listing': Listing_Sitemap(),
    'static': Static_Sitemap(),
    #'blog': Blog_Sitemap(),
}


urlpatterns = [
    path('', include('FunctionModule.pages.urls')),
    path('api/', include('FunctionModule.api.urls')),
    path('blog/', include('FunctionModule.blog.urls')),
    path('listings/', include('FunctionModule.listings.urls')),
    path('realtors/', include('FunctionModule.realtors.urls')),
    path('transactions/', include('FunctionModule.transactions.urls')),
    path('customers/', include('FunctionModule.customers.urls')),
    path('accounts/', include('FunctionModule.accounts.urls')),
    path('cadastral/', include('FunctionModule.cadastral.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('pwa.urls')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = handler404
handler500 = handler500