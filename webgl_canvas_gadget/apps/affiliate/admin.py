from __future__ import unicode_literals

from django.contrib import admin

from .models import Affiliate

class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'affiliate_url')

admin.site.register(Affiliate, AffiliateAdmin)