from __future__ import unicode_literals
import binascii, csv
from django.contrib import admin
from django.http import HttpResponse
from .models import ProjectRequest, ProjectRequestImage, SiteSettings, HomepageRowItem

from django.contrib.admin import SimpleListFilter
    
def null_filter(field, title_=None):
    class NullListFilter(SimpleListFilter):
        parameter_name = field+'__isnull'
        title = title_ or field
        
        def lookups(self, request, model_admin):
            return(
                ('1', 'Null', ),
                ('0', 'Not Null', ),
            )
    
        def queryset(self, request, queryset):
            if self.value() in ('0', '1'):
                kwargs = { self.parameter_name : self.value() == '1' }
                return queryset.filter(**kwargs)
            return queryset
    return NullListFilter

class ProjectRequestImageInline(admin.TabularInline):
    model = ProjectRequestImage
    extra = 0
    
class HomepageRowItemInline(admin.TabularInline):
    model = HomepageRowItem
    extra = 0
    
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [
        HomepageRowItemInline,
    ]

class ProjectRequestAdmin(admin.ModelAdmin):
    inlines = [
        ProjectRequestImageInline,
    ]
    list_display = ('project_name', 'user', 'user_email', 'created_at', 'status', 'project_link', 'signup_link')
    list_filter = ['status', 'created_at', null_filter('user')]
    actions = ['export_as_csv']
    
    def signup_link(self, obj):
        if not obj.user:
            x = binascii.hexlify(bytes(obj.user_email, 'utf-8'))
            x = str(x,'utf-8')
            return '<a href="/signup/?e={0}" target="_blank">signup link</a>'.format(x)
        return ''
    signup_link.short_description = 'signup link'
    signup_link.allow_tags = True
    
    def project_link(self, obj):
        from apps.projects.models import Project
        try:
            return '<a href="/admin/projects/project/{0}" target="_blank">project link</a>'.format(obj.project.id)
        except Project.DoesNotExist:
            return ''
    project_link.short_description = 'project link'
    project_link.allow_tags = True
    
    def export_as_csv(self, request, queryset):
        kwargs = {}
        for f,arg in request.GET.items():
            kwargs.update({f:arg})
        ids = ProjectRequest.objects.filter(**kwargs).distinct('user', 'user_email').order_by('user', 'user_email').values_list('id', flat=True)
        queryset = ProjectRequest.objects.filter(id__in=ids)
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        for obj in queryset:
            writer.writerow([obj.get_email()])
        return response    
    export_as_csv.short_description = "Export as csv"
    
admin.site.register(ProjectRequest, ProjectRequestAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)