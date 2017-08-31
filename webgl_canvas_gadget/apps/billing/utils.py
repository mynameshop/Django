from __future__ import unicode_literals
import stripe
from pinax.stripe.models import Plan
from pinax.stripe import utils as stripe_utils
from .plan_template import PRICING_TEMPLATES

def get_plan_template_by_stripe_id(stripe_id='silver'):
    return PRICING_TEMPLATES.get(stripe_id, 'silver')

def get_plan_by_stripe_id(stripe_id):
    return Plan.objects.get(stripe_id=stripe_id)

def create_plan_from_template(plan_template):
    amount = plan_template.get('subscription_cost', 10) * 100
    data = {
        'amount': amount * 12,
        'interval': "month",
        'interval_count': 12,
        'name': plan_template.get('slug'),
        'currency': "usd",
        'id': plan_template.get('slug')
    }
    try:
        stripe.Plan.create(**data)
    except stripe.InvalidRequestError as e:
        if e._message != 'Plan already exists.':
            raise(e)
    
    stripe_plan = stripe.Plan.retrieve(plan_template.get('slug'))    
    defaults = dict(
        amount = stripe_utils.convert_amount_for_db(stripe_plan["amount"], stripe_plan["currency"]),
        currency = stripe_plan["currency"] or "usd",
        interval = stripe_plan["interval"],
        interval_count = stripe_plan["interval_count"],
        name = stripe_plan["name"],
        statement_descriptor = stripe_plan["statement_descriptor"] or "",
        trial_period_days = stripe_plan["trial_period_days"]
    )
            
    plan, created = Plan.objects.get_or_create(
        stripe_id = stripe_plan["id"],
        defaults = defaults
    )
    stripe_utils.update_with_defaults(plan, defaults, created)
    return plan 

def get_or_create_plan_by_stripe_id(stripe_id):
    try:
        plan = get_plan_by_stripe_id(stripe_id)
    except Plan.DoesNotExist:
        plan_template = get_plan_template_by_stripe_id(stripe_id)
        plan = create_plan_from_template(plan_template)
    return plan

def get_or_create_plan_by_project(project):
    plan_stripe_id = 'silver'
    if project.projectrequest_id:
        plan_stripe_id = project.projectrequest.get_subscription_template_display()
    return get_or_create_plan_by_stripe_id(plan_stripe_id)
    