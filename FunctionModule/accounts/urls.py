from FunctionModule import admin_site
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

admin_site.autodiscover()

urlpatterns = [
    path('register', views.register, name='register'),
    path('register_success', views.register_success, name='register_success'),
    path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="account_login"),
    path('login', views.login_handler, name='login'),
    #path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    #path('logout', auth_views.LogoutView.next_page('/successfully_logged_out/'), name='logout'),
    path('logout', views.logout_handler, name='logout'),
    path("logout/", views.logout, name="account_logout"),
    path('profile', views.profile, name='profile'),
    path('password_change', views.password_change, name='password_change'),
    path("password/change/",views.password_change,name="account_change_password",),
    path("password/set/", views.password_set, name="account_set_password"),
    path("inactive/", views.account_inactive, name="account_inactive"),
    # E-mail
    path("email/", views.email, name="account_email"),
    path("confirm-email/",views.email_verification_sent,name="account_email_verification_sent",),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$",views.confirm_email,name="account_confirm_email",),
    # password reset
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path(
        "password/reset/done/",
        views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),

    #Social App
    path('social/login/cancelled/', views.social_login_cancelled, name="socialaccount_login_cancelled",),
    path('social/login-zalo-callback', views.login_zalo_callback, name='login_zalo'),
    path("social/login/error/", views.login_error, name="socialaccount_login_error"),
    path("social/signup/", views.signup, name="socialaccount_signup"),
    path("social/connections/", views.connections, name="socialaccount_connections"),
]

