from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

admin.autodiscover()

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_handler, name='login_username'),
    #path('logout', auth_views.LogoutView.as_view(next_page='/admin/'), name='logout'),
    path('logout', views.logout_handler, name='logout'),
    path('profile', views.profile, name='profile'),
    path('password_change', views.password_change, name='password_change'),
    path('admin/', admin.site.urls), #for Backend from default lib
    path('social/login/cancelled/', views.social_login_cancelled),
]
