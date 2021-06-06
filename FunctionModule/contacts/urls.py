from django.urls import path

from . import views

urlpatterns = [
    path('contact', views.contact, name='post_contact'),
    path('request_quote', views.request_quote, name='request_quote')
]
