from __future__ import unicode_literals
from django.views.generic import FormView, View, DetailView
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse, Http404

from pinax.stripe.actions.sources import sync_payment_source_from_stripe_data
from pinax.stripe.models import Card, Subscription
from stripe.error import CardError

from . import utils
from .forms import CreditcardForm
from apps.projects.models import Project

import logging
logger = logging.getLogger(__name__) 

class CardListView(View):
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        data = {}
        customer = request.user.get_or_create_customer()
        default_card_token = customer.default_source
        
        card_list = []
        for c in customer.card_set.all():
            card_list.append({
                'id': c.id,
                'last4': c.last4,
            })
        data['card_list'] = card_list
        
        try:
            dc = Card.objects.get(stripe_id=default_card_token)
            data['default_card'] = {
                'id': dc.id,
                'last4': dc.last4,
            }
        except:
            data['default_card'] = None
            
        return JsonResponse(data)
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
class AddCardView(FormView):
    template_name = 'contact.html'
    form_class = CreditcardForm
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({})
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        data = {}
        if request.is_ajax():
            if form.is_valid():
                customer = request.user.get_or_create_customer()
                token = form.cleaned_data['stripe_token']
                
                try:
                    source = customer.stripe_customer.sources.create(source=token)
                except CardError as e:
                    return JsonResponse({'error': {'message': e._message}}, status=500)
#                 except Exception as e:
#                     raise(e)
#                     return JsonResponse({'error': {'message': 'Charge is declined'}}, status=500)
                
                sync_payment_source_from_stripe_data(customer, source)
                
                customer.default_source = source["id"]
                customer.save()
            else:
                errors = []
                for field in form:
                    for error in field.errors:
                        errors.append(error)
                data = {
                    'errors': errors,
                }
        return JsonResponse(data)
    
class ChangeActiveCardView(View):
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({})
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        card_id = request.POST['card']
        customer = request.user.get_or_create_customer()
        card = customer.card_set.get(id=card_id)
        customer.default_source = card.stripe_id
        customer.save()
        
        return JsonResponse({})
   
class ProjectPaymentView(DetailView):
    model = Project
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset().filter(owner=self.request.user)
        return qs
    
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        customer = request.user.get_or_create_customer()
        default_card_token = customer.default_source
        if not default_card_token or not Card.objects.filter(stripe_id=default_card_token).exists():
            raise Http404("card doesn't exist")
         
        obj = self.get_object()
        plan = obj.get_or_create_plan()
        subscription = obj.subscription
         
        action = request.GET.get('action', None)
        if action == 'publish':
            if subscription:
                subscription = request.user.renew_subscription(subscription)
            else:
                try:
                    coupon_stripe_id = obj.coupon.stripe_id if obj.coupon else None
                    subscription = request.user.create_subscription(plan, coupon=coupon_stripe_id)
                    obj.subscription = subscription
                    obj.save()
                except CardError as e:
                    return JsonResponse({'error': {'message': e._message}}, status=500)
                except Exception as e:
                    logger.error('payment error for subscription<{0}>. error message <{1}>'.format(subscription, e))
                    return JsonResponse({'error': {'message': 'Charge was declined.'}}, status=500)
                     
        elif action == 'unpublish':
            if subscription and subscription.customer_id == customer.id:
                request.user.cancel_subscription(subscription)
                subscription.refresh_from_db()
         
        data = {
            'id': obj.id,
            'name': obj.name,
            'subscription_status_display_text': obj.subscription_status_display_text,
            'projectrequest_status': obj.projectrequest_status,
            'subscription_is_active': obj.subscription_is_active,
            'thumbnail': {
                'url': obj.thumbnail.url if obj.thumbnail else '/static/img/project_default.png',
            },
            'subscription': {
                'cancel_at_period_end': 1 if subscription and subscription.cancel_at_period_end else 0
            },
        }
        return JsonResponse(data)