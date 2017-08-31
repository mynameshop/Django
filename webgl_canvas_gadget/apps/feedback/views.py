from __future__ import unicode_literals
from django.views.generic import CreateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import settings

from .models import Feedback
from .forms import FeedbackForm
from apps.canvas_gadget.models import SiteSettings

class FeedbackCreateView(CreateView):
    template_name = 'feedback/create_view.html'
    model = Feedback
    form_class = FeedbackForm
    
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['SITESETTINGS'] = SiteSettings.objects.get(id=settings.SITE_ID)
        return c
    
    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(
            self.get_context_data(
                message = 'Your message has been sent. Thank you for contacting us. We will reply as soon as we can.',
                form = self.get_form(),
            )
        )