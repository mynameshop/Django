from __future__ import unicode_literals

from django.db.models import signals
from django.dispatch import receiver
from .models import Project

@receiver(signals.post_save, sender=Project)
def on_project_changed(sender, **kwargs):
    if kwargs['created']:
        kwargs['instance'].get_or_create_plan()