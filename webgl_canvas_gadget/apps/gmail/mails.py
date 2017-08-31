from __future__ import unicode_literals
from .utils import GMail
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template

def get_absolute_url(path):
    from django.contrib.sites.models import Site
    site = Site.objects.get_current().domain
    return 'http://{site}{path}'.format(site=site, path=path)

def send_projectrequest_success_for_new_user(to):
    import binascii
    e_key = str( binascii.hexlify(bytes(to, 'utf-8') ), 'utf-8')
    url = '{0}?next={1}&e={2}'.format(
        get_absolute_url(reverse('accounts:signup')),
        reverse('projects:list_view'),
        e_key
    )
    
    context = {
        'url_track_project': url,
        'username': to
    }
    message_text = get_template('gmail/projectrequest_success_for_new_user.html').render(context)
    g = GMail()
    g.send_email(to, 'You Project Has Been Submitted', message_text)