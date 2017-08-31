from __future__ import unicode_literals
from django.http import HttpResponse, Http404

def active_subscription_or_sample_required(func, redirect_url='/'):
    def check_and_call(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        
        import importlib 
        from django.core.urlresolvers import resolve
        from apps.sample.models import Sample
        
        view_func = resolve(request.path).func
        module = importlib.import_module(view_func.__module__)
        
        _view = getattr(module, view_func.__name__)
        model = getattr(_view, 'model', None)
        
        if not model: 
            return Http404()
        
        obj = None
        if 'pk' in kwargs:
            obj = model.objects.get(pk=kwargs["pk"])
        elif 'slug' in kwargs:
            obj = model.objects.get(slug=kwargs["slug"])
            
        if obj.subscription_is_active or Sample.objects.filter(project = obj).count() > 0:
            return func(request, *args, **kwargs)
        
        return HttpResponse("Subscription of this project is not active", status=403)
    return check_and_call