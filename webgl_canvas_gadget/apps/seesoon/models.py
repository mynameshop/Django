from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.base.models import ModelCreatetAtMixin

class Subscription(ModelCreatetAtMixin):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    
    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        ordering = ['id',]
        
    def __str__(self):
        return self.email