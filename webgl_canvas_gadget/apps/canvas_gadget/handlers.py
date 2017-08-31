from __future__ import unicode_literals

from django.db.models import signals
from django.dispatch import receiver
from .models import ProjectRequest

@receiver(signals.post_save, sender=ProjectRequest)
def on_projectrequest_changed(sender, **kwargs):
    if kwargs['created']:
        kwargs['instance'].get_or_create_project()
    else:
        p = kwargs['instance'].get_or_create_project()
        if p and kwargs['instance'].user_id and p.owner_id != kwargs['instance'].user_id:
            p.owner = kwargs['instance'].user
            p.save()