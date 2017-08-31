from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve
from django.core.urlresolvers import Resolver404
from profiles import wedge_helper as wh
   

class FbWedgeCheckMiddleware(object):
    def process_response(self, request, response):
       
        try:
            url_name = resolve(request.path_info).url_name
        except Resolver404:
            url_name = None
        wh.is_wedge_eligible(request)
        exclude_routes = [
            'wedge',
            'faq',
        ]
        if url_name not in exclude_routes and \
            not request.path.startswith(reverse('admin:index')) and \
            wh.is_wedge_eligible(request): 
                return redirect(reverse('profiles:wedge'))
        else:
                return response