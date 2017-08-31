from __future__ import unicode_literals
from django.contrib import admin
from .models import SiteDemo

class SiteDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(SiteDemo, SiteDemoAdmin)