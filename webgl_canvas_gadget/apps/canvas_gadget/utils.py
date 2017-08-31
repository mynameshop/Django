from django.contrib.sites.shortcuts import get_current_site
from settings import SITE_ABSOLUTE_URL_PATTERT

def get_absolute_url(url):
    return SITE_ABSOLUTE_URL_PATTERT.format(get_current_site(None).domain, url) 