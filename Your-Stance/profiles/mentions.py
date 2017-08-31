import itertools
import re
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe

import notifications.models as nmodels
from notifications.models import Notification
from notifications import helper as nh
from notifications import models as nm


def parse_mention_text(text, unique=False):

    found = []
    splitted = text.split()

    for x in splitted:
        if not x.startswith("@"):
            continue
        x = x.replace('@', '').replace(' ', '').replace(',', '').replace(';', '').replace('.', '').replace('-', '')
        found.append(x)

    if unique:
        return list(set(found))
    else:
        return found


def mentions_to_hrefs(text):
    """
    Unused. Mention replacing moved to JS.
    """
    mentions = parse_mention_text(text, unique=False)
    hrefed_text = text

    for m in mentions:
        try:
            user = User.objects.get(username=m)
            mm = '@'+m
            url = '/'+m
            hrefed_text = hrefed_text.replace(mm, '<a href="'+url+'">'+mm+'</a>')
        except User.DoesNotExist:
            pass

    return hrefed_text


def get_mentioned_users(text):
    mentioned = parse_mention_text(text)
    mentioned_users = []
    for username in mentioned:
        mentioned_users += User.objects.filter(username=username)

    return mentioned_users


def mention(text, mentioner, stance_comment=None, stance=None, comment=None, notification_type=nmodels.MENTION):
    mentioned = get_mentioned_users(text)

    for m in mentioned:
        nh.send_notification(type=notification_type, user_from=mentioner, user_to=m, stance=stance, comment=comment)
