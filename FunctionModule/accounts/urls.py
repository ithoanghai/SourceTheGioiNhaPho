from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

admin.autodiscover()

urlpatterns = [
    path('register', views.register, name='register'),
    path('register_success', views.register_success, name='register_success'),
    path('login', views.login_handler, name='login'),
    #path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    #path('logout', auth_views.LogoutView.next_page('/successfully_logged_out/'), name='logout'),
    path('logout', views.logout_handler, name='logout'),
    path('profile', views.profile, name='profile'),
    path('password_change', views.password_change, name='password_change'),
    path('social/login/cancelled/', views.social_login_cancelled),
    path('social/login-zalo-callback', views.login_zalo_callback, name='login_zalo'),
]
