import debug_toolbar
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    path('', include('FunctionModule.pages.urls')),
    path('api/', include('FunctionModule.api.urls')),
    path('listings/', include('FunctionModule.listings.urls')),
    path('transactions/', include('FunctionModule.transactions.urls')),
    path('accounts/', include('FunctionModule.accounts.urls')),
    path('contacts/', include('FunctionModule.contacts.urls')),
    path('cadastral/', include('FunctionModule.cadastral.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
