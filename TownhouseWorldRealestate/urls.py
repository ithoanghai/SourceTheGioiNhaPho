from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('FunctionModule.pages.urls')),
    path('listings/', include('FunctionModule.listings.urls')),
    path('accounts/', include('FunctionModule.accounts.urls')),
    path('contacts/', include('FunctionModule.contacts.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)