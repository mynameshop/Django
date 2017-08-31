from __future__ import unicode_literals
from apps.base.decorators import jinja2_global
from .models import Sample

@jinja2_global
def get_random_samples(limit=2, show_on_main=True):
    return list(Sample.objects.filter(is_main=False, show_on_main=show_on_main).distinct().select_related('project').order_by('?')[:limit])