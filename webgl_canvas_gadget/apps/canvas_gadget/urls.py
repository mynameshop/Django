from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='homepage'),
    url(r'^pricing/$', views.PricingPageView.as_view(), name='pricingpage'),
    url(r'^submitproject/$', views.SubmitProjectView.as_view(), name='submitproject'),
    url(r'^submitproject/success/$', views.SubmitProjectSuccessView.as_view(), name='submitproject_success'),
    
    url(r'^robots\.txt$', TemplateView.as_view(template_name='canvas_gadget/robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='canvas_gadget/sitemap.xml', content_type='text/xml')),
    url(r'^ror\.xml$', TemplateView.as_view(template_name='canvas_gadget/ror.xml', content_type='text/xml')),
]
