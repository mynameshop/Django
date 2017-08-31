from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import Subscription
from apps.base.forms import AjaxableResponseMixin

class SeeSoon(TemplateView):
    template_name = 'seesoon/index.html'
    
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return super().get(request,  *args, **kwargs)
    
class SubscriptionCreateView(CreateView, AjaxableResponseMixin):
    model = Subscription
    fields = ('name', 'email')
    template_name = 'seesoon/index.html'
    
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('canvas_gadget:homepage')