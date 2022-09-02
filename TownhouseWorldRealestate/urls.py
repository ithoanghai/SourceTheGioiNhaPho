import debug_toolbar
from importlib import import_module

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from FunctionModule.accounts import providers
from FunctionModule import admin_site
from FunctionModule.admin_site.sites import AdminSitePlus
#from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()
admin.site.site_header = 'Quản trị hệ thống thế giới nhà phố'


def redirect_view(request):
    response = redirect('/admin_site/')
    return response


urlpatterns = [
    path('', include('FunctionModule.pages.urls')),
    path('api/', include('FunctionModule.api.urls')),
    path('blog/', include('FunctionModule.blog.urls')),
    path('listings/', include('FunctionModule.listings.urls')),
    path('transactions/', include('FunctionModule.transactions.urls')),
    path('customers/', include('FunctionModule.customers.urls')),
    path('accounts/', include('FunctionModule.accounts.urls')),
    path('cadastral/', include('FunctionModule.cadastral.urls')),
    path('admin_site', redirect_view, name='admin'),
    path('admin_site/', admin_site.site.urls),
    #path('admin/', site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


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