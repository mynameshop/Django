from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.SiteDemoDetailView.as_view(), name='detail_view'),
    url(r'^(?P<slug>[-\w]+)/$', views.SiteDemoDetailView.as_view(), name='detail_view'),
]
