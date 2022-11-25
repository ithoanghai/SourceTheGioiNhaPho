from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Url for FrontEnd
    path('', views.home_view, name='index'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('about', views.about, name='about'),
    path('message', views.message, name='message'),
    # Matches any html file
    # re_path('^.*\.*', views.pages, name='pages'),
    # url menu

    path('specialistUs', views.specialist_us, name='specialist_us'),
    path('specialist', views.specialist, name='specialist'),
    path('specialist/<int:realtor_id>', views.specialist_detail, name='specialistDetail'),
    path('whychoose', views.whychoose, name='whychoose'),
    path('services', views.services, name='services'),
    path('contacts', views.contacts, name='contacts'),
    path('recruitment', views.recruitment, name='recruitment'),
    path('termsOfUse', views.termsOfUse, name='termsOfUse'),
    path('privacyPolicy', views.privacyPolicy, name='privacyPolicy'),
    path('page-not-found-test', views.error404, name='page-not-found-test'),

    # Url for Backend
    path('admin/map', views.map, name='map'),
    path('admin/table', views.table, name='table'),
    path('admin/chart', views.chart, name='chart'),
    path('admin/pageblank', views.pageblank, name='page-blank'),

    path('admin/error403', views.error403, name='error403'),
    path('admin/error404', views.error404, name='error404'),
    path('admin/error500', views.error500, name='error500'),

    # for our built-in ajax post view
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

]