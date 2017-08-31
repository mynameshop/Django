from __future__ import unicode_literals
from django.db import models
from apps.base.models import ModelCreatetAtMixin
from tinymce.models import HTMLField

class SiteDemo(ModelCreatetAtMixin):
    slug = models.SlugField()
    description = models.CharField(max_length=256, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    website_screenshot = models.ImageField(upload_to = 'demobooth')
    
    website_extra_html = HTMLField(
        max_length=2048,
        default='<iframe src="/" frameborder="0" style="position: absolute; top: 232px; left: 337px; width: 497px; height: 223px;"></iframe>'
    )
    
    def __str__(self):
        return '{0} ({1}) - '.format(self.slug, self.website_url)