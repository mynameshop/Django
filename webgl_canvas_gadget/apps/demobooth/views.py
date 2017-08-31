from __future__ import unicode_literals
from django.views.generic import DetailView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import SiteDemo

class SiteDemoDetailView(DetailView):
    template_name = 'demobooth/detail_view.html'
    model = SiteDemo
    
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        return c