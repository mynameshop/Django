from __future__ import unicode_literals
from django.contrib import admin
from .models import Sample

class SampleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sample, SampleAdmin)