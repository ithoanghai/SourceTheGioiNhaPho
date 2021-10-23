from django.urls import path
from .views import get_states, search_listing, download_exported_listing, get_user

urlpatterns = [
    path('s-suggest/<str:action>/<str:lookup>', get_states),
    path('search', search_listing),
    path('download_fb_export', download_exported_listing),
    path('current_user', get_user)
]
