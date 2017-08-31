# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(), name='list_view'),
    
    url(r'^(?P<pk>\d+)/$', views.ProjectNewDetailView.as_view(), name='detail_view'),
    url(r'^(?P<slug>[-\w]+)/$', views.ProjectNewDetailView.as_view(), name='detail_view'),
    url(r'^(?P<pk>\d+)/compact/$', views.ProjectNewDetailCompactView.as_view(), name='detail_compact_view'),
    url(r'^(?P<slug>[-\w]+)/compact/$', views.ProjectNewDetailCompactView.as_view(), name='detail_compact_view'),
    
#     url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detail_view'),
#     url(r'^(?P<pk>\d+)/base/$', views.ProjectDetailBaseView.as_view(), name='detail_base_view'),
#     url(r'^(?P<pk>\d+)/compact/$', views.ProjectDetailCompactView.as_view(), name='detail_compact_view'),
    url(r'^(?P<pk>\d+)/edit/$', views.ProjectEditView.as_view(), name='edit_view'),
#     url(r'^(?P<slug>[-\w]+)/$', views.ProjectDetailView.as_view(), name='detail_view'),
#     url(r'^(?P<slug>[-\w]+)/base/$', views.ProjectDetailBaseView.as_view(), name='detail_base_view'),
#     url(r'^(?P<slug>[-\w]+)/compact/$', views.ProjectDetailCompactView.as_view(), name='detail_compact_view'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.ProjectEditView.as_view(), name='edit_view'),
    
    url(r'^model/create/$', views.Model3dCreateView.as_view(), name='model3d_create_view'),
    url(r'^model/(?P<pk>\d+)/edit/$', views.Model3dEditView.as_view(), name='model3d_edit_view'),
    url(r'^model/(?P<pk>\d+)/edit/gallery/$', views.Model3DGalleryView.as_view(), name='model3d_gallery_view'),
    
    url(r'^animation/(?P<pk>\d+)/edit/$', views.AnimationEditView.as_view(), name='animation_edit_view'),
]
