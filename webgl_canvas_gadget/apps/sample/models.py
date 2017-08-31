from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from apps.base.models import ModelCreatetAtMixin
from apps.projects.models import Project

class Sample(ModelCreatetAtMixin):
    project = models.OneToOneField(Project)
    show_on_main = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    description = models.CharField(max_length=256)
    
    class Meta:
        verbose_name = _('sample')
        verbose_name_plural = _('samples')
        ordering = ['id',]
        
    def __str__(self):
        return 'sample ({0})'.format(self.project.__str__())
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.is_main:
            Sample.objects.filter(is_main=True).update(is_main=False)
        super().save(*args, **kwargs)