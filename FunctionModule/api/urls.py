from django.urls import path
from .views import get_states, search_listing

urlpatterns = [
    path('s-suggest/<str:action>/<str:lookup>', get_states),
    path('search', search_listing)
]
