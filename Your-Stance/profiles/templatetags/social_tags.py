from django import template
from allauth.socialaccount import models

register = template.Library()

@register.assignment_tag
def fb_appid(*args, **kwargs):
    return  models.SocialApp.objects.get_current('facebook').client_id
    


