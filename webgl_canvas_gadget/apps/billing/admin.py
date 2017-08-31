from __future__ import unicode_literals
from django.contrib import admin
from pinax.stripe.models import Subscription, Plan

class AdminSubscription(admin.ModelAdmin):
    readonly_fields = [
        'customer', 'stripe_id', 'status',
    ]
    fields = [
        'plan', 'customer', 'stripe_id', 'status',
    ]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'plan':
            kwargs['queryset'] = Plan.objects.filter(stripe_id__in=['silver', 'gold', 'platinum'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.save()
        from pinax.stripe.actions import subscriptions
        subscriptions.update(obj, plan = obj.plan)

admin.site.register(Subscription, AdminSubscription)