from ajax_select import urls as ajax_select_urls
from django.urls import path, include

urlpatterns = [
    path('', include(ajax_select_urls), name="cadastral_ajax_select"),
]
