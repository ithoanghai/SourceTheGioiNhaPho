from django.urls import re_path

from . import views
from .views import IndexView, PostDetailJSONView, PostDetailView, PostCountHitDetailView

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name="blogs"),

    re_path(r'^generic-detail-view-ajax/(?P<pk>\d+)/$',
        PostDetailJSONView.as_view(), name="ajax"),
    re_path(r'^hitcount-detail-view/(?P<pk>\d+)/$',
        PostDetailView.as_view(), name="detail"),
    re_path(r'^hitcount-detail-view-count-hit/(?P<pk>\d+)/$',
        PostCountHitDetailView.as_view(), name="detail-with-count"),

]