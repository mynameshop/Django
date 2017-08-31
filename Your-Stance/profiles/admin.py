from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, ProfileVerification, Follow
from profiles.forms import VerificationAdminForm

class ProfileVerificationInline(admin.StackedInline):
    model = ProfileVerification
    extra = 0
    max_num = 0
    form = VerificationAdminForm



# Define an inline admin descriptor for UserProfile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileVerificationAdmin(admin.ModelAdmin):

    
    model = ProfileVerification
    list_display = ['user', 'status', 'created' , 'modified', ]
    list_filter = ['status', ]
    ordering = ['-created']
    fields = ['user', 'photo', 'status', ]
    readonly_fields = ['user', 'photo', ]
    change_form_template = 'profiles/admin/change_form.html'
    
    
    def has_add_permission(self, request):
        return False
    
    def get_urls(self):
        urls = super(ProfileVerificationAdmin, self).get_urls()
        
        add_urls = [
                           url(r'(?P<id>\d+)/approve/$',
                            self.admin_site.admin_view(self.approve), name="verify_approve"),
        ]
        return add_urls + urls
    
    def approve(self, request, id):
        verification = ProfileVerification.objects.get(pk=id)
        verification.status = ProfileVerification.STATUS_VERIFIED
        verification.save()
        return redirect(request.META['HTTP_REFERER'])

# Define a new User admin
class MyUserAdmin(UserAdmin):
    inlines = (ProfileInline, ProfileVerificationInline, )
    list_display = ("username", "email", "is_active", "is_staff")

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(ProfileVerification, ProfileVerificationAdmin)


