from django.contrib import admin
from django.urls import path

# from django.contrib.auth import views as auth_views
from . import views

admin.autodiscover()

urlpatterns = [
    path('login', views.login_handler, name='login_username'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('social/login/cancelled/', views.social_login_cancelled),
]
