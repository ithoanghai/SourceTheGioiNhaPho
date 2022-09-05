from django.conf.urls import include, url

from . import views
from .views import IndexView, PostDetailJSONView, PostDetailView, PostCountHitDetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="blogs"),

    url(r'^generic-detail-view-ajax/(?P<pk>\d+)/$',
        PostDetailJSONView.as_view(), name="ajax"),
    url(r'^hitcount-detail-view/(?P<pk>\d+)/$',
        PostDetailView.as_view(), name="detail"),
    url(r'^hitcount-detail-view-count-hit/(?P<pk>\d+)/$',
        PostCountHitDetailView.as_view(), name="detail-with-count"),

]