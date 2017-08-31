from __future__ import unicode_literals
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import settings

from .models import SiteSettings
from apps.billing.plan_template import PRICING_TEMPLATES
from .forms import ProjectRequestForm
from django.core.urlresolvers import reverse
from apps.sample.models import Sample
from apps.gmail import mails

class HomePageView(TemplateView):
    template_name = 'canvas_gadget/homepage.html'
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['SITESETTINGS'] = SiteSettings.objects.get(id=settings.SITE_ID)
        return c
    
class PricingPageView(TemplateView):
    template_name = 'canvas_gadget/pricingpage.html'
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['PRICING_TEMPLATES'] = PRICING_TEMPLATES
        if 'sample' in self.request.GET:
            try:
                c['SAMPLE'] = Sample.objects.get(id = self.request.GET['sample'])
            except:
                pass
        return c
    
class SubmitProjectView(FormView):
    template_name = 'canvas_gadget/submitproject.html'
    form_class = ProjectRequestForm
    object = None
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['PRICING_TEMPLATES'] = PRICING_TEMPLATES
        c['ACTIVE_PRICING_TEMPLATE'] = PRICING_TEMPLATES.get(
            self.request.GET.get('s', 'silver'), 
            PRICING_TEMPLATES.get('silver')
        )
        return c
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form_kwargs = self.get_form_kwargs()
        if self.request.user.is_authenticated():
            form_kwargs['initial']['user_email'] = self.request.user.email or self.request.user.username
            form_kwargs['initial']['user'] = self.request.user.id
        f = form_class(**form_kwargs)
        return f
    
    def form_valid(self, form):
        self.object = form.save_all()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_success_url(self):
        url = reverse('canvas_gadget:submitproject_success')
        if not self.request.user.is_authenticated():
            if self.object.user_email:
                import binascii
                e_key = str( binascii.hexlify(bytes(self.object.user_email, 'utf-8') ), 'utf-8')
                url = url + '?e=' + e_key
                mails.send_projectrequest_success_for_new_user(self.object.user_email)
        return url

class SubmitProjectSuccessView(TemplateView):
    template_name = 'canvas_gadget/submitproject_success.html'
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['e_key'] = self.request.GET.get('e', None)
        return c
    
class DeployView(TemplateView):
    template_name = 'canvas_gadget/waiting_deploy.html'
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        from settings import DEPLOY_SCRIPT_PATH
        import os, subprocess
        
        if len(DEPLOY_SCRIPT_PATH) > 0 and os.path.isfile(DEPLOY_SCRIPT_PATH) :
            subprocess.call([DEPLOY_SCRIPT_PATH], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                shell=True)
        return super().get(request,  *args, **kwargs)