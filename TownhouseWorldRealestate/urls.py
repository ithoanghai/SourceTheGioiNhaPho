import debug_toolbar
from importlib import import_module

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.views.static import serve

from FunctionModule.accounts import providers
from FunctionModule import admin_site
from FunctionModule.admin_site.sites import AdminSitePlus
from django.contrib.sitemaps.views import sitemap

from FunctionModule.pages.sitemaps import Listing_Sitemap, Static_Sitemap
from FunctionModule.pages.views import handler404, handler500
from TownhouseWorldRealestate import settings

admin.site = AdminSitePlus()
admin.autodiscover()
admin.site.site_header = 'Quản trị hệ thống thế giới nhà phố'

sitemaps = {
    'listing': Listing_Sitemap(),
    'static': Static_Sitemap(),
}

def redirect_view(request):
    response = HttpResponseRedirect('/admin/')
    return response


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
    path('admin', redirect_view, name='admin'),
    path('admin/', admin_site.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]


# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns

handler404 = handler404
handler500 = handler500