# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_cleanup.signals import cleanup_pre_delete

class ModelCreatetAtMixin(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, auto_now=False, editable=False, db_index=True)
    
    class Meta:
        abstract = True

class ModelDatetimeMixin(ModelCreatetAtMixin):
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=False, auto_now=True, editable=False, db_index=True)
    
    class Meta:
        abstract = True

def sorl_delete(**kwargs):
    from easy_thumbnails.files import get_thumbnailer
    thumbnailer = get_thumbnailer(kwargs['file'])
    thumbnailer.delete_thumbnails()

cleanup_pre_delete.connect(sorl_delete)
