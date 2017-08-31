# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^card/add/$', views.AddCardView.as_view(), name='card_add_view'),
    url(r'^card/change_active/$', views.ChangeActiveCardView.as_view(), name='change_active_card_view'),
    url(r'^card/$', views.CardListView.as_view(), name='card_list_view'),
    
    url(r'^project/(?P<pk>\d+)/$', views.ProjectPaymentView.as_view(), name='project_payment_view'),
]
