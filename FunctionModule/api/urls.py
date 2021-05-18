from django.urls import path
from .views import get_states

urlpatterns = [
    path('s-suggest/<str:action>/<str:lookup>', get_states)
]
