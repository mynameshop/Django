from __future__ import unicode_literals
from django.conf.urls import url, include
from .api_v1 import api_v1

urlpatterns = [
   url('', include(api_v1.urls) ),
]
