from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.affiliate.models import Affiliate

class User(AbstractUser):
    
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    
    class Meta:
        db_table = 'auth_user'
        
    def get_or_create_customer(self):
        import stripe
        from pinax.stripe.models import Customer
        from pinax.stripe.actions.customers import sync_customer
        try:
            customer = self.customer
        except Customer.DoesNotExist:
            stripe_customer = stripe.Customer.create(
                email=self.email,
            )
            customer = Customer.objects.create(
                user = self,
                stripe_id = stripe_customer["id"]
            )
            sync_customer(customer, stripe_customer)
        return customer
    
    def create_subscription(self, plan, default_card_token=None, coupon=None):
        from pinax.stripe.actions.subscriptions import create
        customer = self.get_or_create_customer()
        subscription = create(customer, plan, token=default_card_token, coupon=coupon)
        return subscription
    
    def renew_subscription(self, subscription):
        from pinax.stripe.actions.subscriptions import sync_subscription_from_stripe_data
        customer = self.get_or_create_customer()
        stripe_subscription = subscription.stripe_subscription
        sub = stripe_subscription.save() 
        return sync_subscription_from_stripe_data(customer, sub)
    
    def cancel_subscription(self, subscription, at_period_end=True):
        from pinax.stripe.actions.subscriptions import cancel
        cancel(subscription, at_period_end=at_period_end)
    
    def active_subscriptions_by_plan(self):
        from pinax.stripe.models import Subscription
        res = {}
        qs = Subscription.objects.filter(customer = self.get_or_create_customer(), status='active').select_related('plan__project')
        for obj in qs:
            res[obj.plan.project.id] = obj
        return res