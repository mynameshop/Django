from __future__ import unicode_literals
from django.apps import AppConfig

class BillingConfig(AppConfig):
    name = 'apps.billing'
    
    def ready(self):
        from .plan_template import PRICING_TEMPLATES
        from .utils import get_or_create_plan_by_stripe_id
        for key in PRICING_TEMPLATES:
            try:
                get_or_create_plan_by_stripe_id(key)
            except:
                pass