import debug_toolbar
from django.conf.urls import url
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()
admin.site.site_header = 'Quản trị hệ thống thế giới nhà phố'

def redirect_view(request):
    response = redirect('/admin/')
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
    path('accounts/', include('allauth.urls')),
    path('admin', redirect_view, name='admin'),
    path('admin/', admin.site.urls),
    #path('admin/', site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
