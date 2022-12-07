from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView

from TownhouseWorldRealestate import settings
from . import views
from .views import handler404, handler500

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

    path('specialistus', views.specialistus, name='specialistus'),
    path('specialist', views.specialist, name='specialist'),
    path('specialist/<int:realtor_id>', views.specialist_detail, name='specialistDetail'),
    path('whychoose', views.whychoose, name='whychoose'),
    path('services', views.services, name='services'),
    path('contacts', views.contacts, name='contacts'),
    path('recruitment', views.recruitment, name='recruitment'),
    path('termsofuse', views.termsofuse, name='termsofuse'),
    path('privacypolicy', views.privacypolicy, name='privacypolicy'),

    # Url for Backend
    path('admin/map', views.map, name='map'),
    path('admin/table', views.table, name='table'),
    path('admin/chart', views.chart, name='chart'),
    path('admin/pageblank', views.pageblank, name='page-blank'),

    path('admin/error403', views.error403, name='error403'),
    path('admin/error404', views.error404, name='error404'),
    path('admin/error500', views.error500, name='error500'),

    # for our built-in ajax post view
    path(r'hitcount/', include('FunctionModule.hitcount.urls', namespace='hitcount')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
