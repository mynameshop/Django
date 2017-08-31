from __future__ import unicode_literals
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
import binascii
from .forms import SignupForm
from apps.canvas_gadget.models import ProjectRequest
   
class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = '/projects/'
    
    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('e', None):
            initial['username'] = str( binascii.unhexlify(self.request.GET.get('e', None)), 'utf-8' )
            initial['e_key'] = self.request.GET.get('e', None)
        return initial
    
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('e', None):
            from django.contrib.auth import get_user_model
            username = str( binascii.unhexlify(self.request.GET.get('e', None)), 'utf-8' )
            if get_user_model().objects.filter(username = username).count() > 0:
                next_url = 'next={0}'.format(self.request.GET.get('next', settings.LOGIN_REDIRECT_URL))
                return redirect('{0}?{1}'.format(reverse('accounts:login'), next_url))
        return super().get(request, args, kwargs)
    
    def get_affiliate(self):
        affiliate = None
        affiliate_key = getattr(self.request, 'affiliate', None)
        if affiliate_key:
            try:
                from apps.affiliate.models import Affiliate
                affiliate = Affiliate.objects.get(pk=affiliate_key)
            except:
                pass
        return affiliate
    
    def set_affiliate(self, user):
        affiliate = self.get_affiliate()
        if affiliate:
            user.affiliate = affiliate
            user.save()

    def form_valid(self, form):
        form.save()
        
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password1']
        )
        
        self.set_affiliate(user)
            
        e_key = form.cleaned_data['e_key']
        if e_key:
            user_email = str( binascii.unhexlify(e_key), 'utf-8' )
            for project_request in ProjectRequest.objects.filter(user_email=user_email, user__isnull=True):
                project_request.user = user
                project_request.save()
        if user:
            login(self.request, user)
            try:
                #создаём заказчика в страйпе
                user.get_or_create_customer()
            except:
                pass
        return super(SignupView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        if self.request.GET.get('next', None) and self.request.GET.get('next').startswith('/'):
            return self.request.GET.get('next')
        return super().get_success_url()