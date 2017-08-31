from django.conf.urls import url

from . import views

app_name = 'pages'

urlpatterns = [
    url(r'^rules$', views.RulesView.as_view(), name='rules'),
    url(r'^tos$', views.TosView.as_view(), name='tos'),
    url(r'^privacy$', views.PrivacyView.as_view(), name='privacy'),
    url(r'^faq$', views.FaqView.as_view(), name='faq'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^finish$', views.FinishView.as_view(), name='finish'),
    url(r'^what/the$', views.WhatTheView.as_view(), name='whatthe'),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
]
