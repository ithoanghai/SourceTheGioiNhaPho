from django.urls import path, re_path
from . import views

urlpatterns = [
    #Url for FrontEnd
    path('', views.index, name ='index'),
    path('about', views.about, name ='about'),
    # Matches any html file
    #re_path('^.*\.*', views.pages, name='pages'),

    #Url for Backend
    #path('admin/', admin.site.urls), #for Backend from default lib
    path('admin/', views.dashboard , name ='dashboard'),
    path('admin/layout1', views.layout1, name='layout1'),
    path('admin/layout2', views.layout2, name='layout2'),
    path('admin/map', views.map , name ='map'),
    path('admin/profile', views.profile , name ='profile'),
    path('admin/table', views.table , name ='table'),
    path('admin/chart', views.chart, name='chart'),
    path('admin/pageblank', views.pageblank, name='page-blank'),


    path('admin/error403', views.error403, name='error403'),
    path('admin/error404', views.error404, name='error404'),
    path('admin/error500', views.error500, name='error500'),

]
