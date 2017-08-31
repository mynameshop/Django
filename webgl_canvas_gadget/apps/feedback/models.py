from __future__ import unicode_literals
from django.db import models
from apps.base.models import ModelCreatetAtMixin

class Feedback(ModelCreatetAtMixin):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    text = models.TextField()
    
    def __str__(self):
        return '{0} ({1}) - '.format(self.email, self.name)