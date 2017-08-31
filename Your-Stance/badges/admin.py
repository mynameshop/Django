from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect
from django.db.models import Q

from badges.models import Badge, ProfileBadge
from badges import helper as bh
from profiles.models import Profile

class ProfileBadgeAdmin(admin.ModelAdmin):
    change_list_template = 'badges/admin/change_list.html'
    list_display = ['badge', 'profile']
    
    def get_urls(self):
        urls = super(ProfileBadgeAdmin, self).get_urls()
        
        add_urls = [
                           url(r'sync/$',
                            self.admin_site.admin_view(self.sync), name="sync_badges"),
        ]
        return add_urls + urls
    
    def sync(self, request):

        profiles = Profile.objects.filter(~Q(user=None) & Q(is_proxy=False)).order_by('created')
        for profile in profiles:
            bh.sync_badges(profile)
        return redirect('/admin/badges/profilebadge/')
    
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['title','type']

admin.site.register(Badge, BadgeAdmin)
admin.site.register(ProfileBadge, ProfileBadgeAdmin)