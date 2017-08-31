from __future__ import unicode_literals

import time

from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponsePermanentRedirect
from django.utils.http import cookie_date


class AffiliateMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        
    def is_valid(self, request):
        ignored_views = ['django.views.static.serve']
        return not request.is_ajax() and resolve(request.path).view_name not in ignored_views

    def process_request(self, request):
        if not self.is_valid(request):
            return
        if request.user.is_anonymous():
            affiliate_key = request.COOKIES.get(
                settings.AFFILIATE_COOKIE_NAME,
                request.GET.get(settings.AFFILIATE_GET_NAME, None)
            )
            setattr(request, 'affiliate', affiliate_key)
        
        if request.GET.get(settings.AFFILIATE_GET_NAME, None):
            return HttpResponsePermanentRedirect(request.path)

    def process_response(self, request, response):
        if not self.is_valid(request):
            return response
        
        if request.user.is_anonymous():
            affiliate_key = getattr(request, 'affiliate', None)
            if affiliate_key:
                max_age = settings.AFFILIATE_COOKIE_AGE
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)
                
                response.set_cookie(
                    settings.AFFILIATE_COOKIE_NAME,
                    affiliate_key,
                    max_age=max_age,
                    expires=expires, 
                    domain=settings.AFFILIATE_COOKIE_DOMAIN,
                    path=settings.AFFILIATE_COOKIE_PATH,
                    secure=settings.AFFILIATE_COOKIE_SECURE or None,
                    httponly=settings.AFFILIATE_COOKIE_HTTPONLY or None,
                )
                
        elif settings.AFFILIATE_COOKIE_NAME in request.COOKIES:
            response.delete_cookie(
                settings.AFFILIATE_COOKIE_NAME,
                path=settings.AFFILIATE_COOKIE_PATH,
                domain=settings.AFFILIATE_COOKIE_DOMAIN,
            )
        return response
