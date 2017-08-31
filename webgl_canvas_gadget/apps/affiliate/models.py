from __future__ import unicode_literals

from django.db import models
from apps.base.models import ModelCreatetAtMixin
from apps.canvas_gadget.utils import get_absolute_url

class Affiliate(ModelCreatetAtMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(blank=True, null=True, max_length=64)
    surname = models.CharField(blank=True, null=True, max_length=64)
    
    def __str__(self):
        return self.email
    
    @property
    def key(self):
        return self.id
    
    @property
    def affiliate_url(self):
        import settings
        url = '/?{0}={1}'.format(settings.AFFILIATE_GET_NAME, self.key)
        return get_absolute_url(url)
    