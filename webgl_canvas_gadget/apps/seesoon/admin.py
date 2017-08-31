from __future__ import unicode_literals
import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Subscription

class SubscriptionAdmin(admin.ModelAdmin):
    actions = ['export_as_csv']
    
    def export_as_csv(self, request, queryset):
        kwargs = {}
        for f,arg in request.GET.items():
            kwargs.update({f:arg})
        ids = queryset.model.objects.filter(**kwargs).distinct('email').order_by('email',).values_list('id', flat=True)
        queryset = queryset.model.objects.filter(id__in=ids)
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        for obj in queryset:
            writer.writerow([obj.email])
        return response    
    export_as_csv.short_description = "Export as csv"
    
admin.site.register(Subscription, SubscriptionAdmin)