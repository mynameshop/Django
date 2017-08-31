from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SeeSoon.as_view(), name='seesoon'),
    url(r'^subscribe/$', views.SubscriptionCreateView.as_view(), name='subscribe'),
]
