# -*- coding: utf-8 -*-

import hashlib
import time
import urllib2

import profiles.models as profile_models
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from profiles import wedge_helper as wh
from profiles.mentions import mention
from profiles.models import Profile
from profiles.slug import make_slug_username
from stances.models import Stance


def handle_avatar(profile, account):
    imageurl = "http://graph.facebook.com/{}/picture?width=512&height=512".format(account.uid)
    m = hashlib.md5()
    m.update(str(time.time()))
    file_name = m.hexdigest() + '.jpg'
    image_file = default_storage.open(file_name, 'w')
    response = urllib2.urlopen(imageurl)
    image = response.read()
    image_file.write(image)
    image_file.close()
    image_file = default_storage.open(file_name, 'r')
    profile.avatar = image_file
    image_file.close()


@receiver(pre_save, sender=User)
def user_save_callback(instance, sender, *args, **kwargs):
    instance.username = str(make_slug_username(instance.username, instance))


redirect_to_follow = False


@receiver(pre_social_login)
def handle_pre_login(request, sociallogin, **kwargs):
    redirect_to_follow = request.session.get('fb_follow_friends', False)

    try:
        user = User.objects.get(email=sociallogin.user.email)
    except User.DoesNotExist:
        user = None
    except User.MultipleObjectsReturned:
        user = None

    if not request.user.is_anonymous():
        user = request.user

    if sociallogin.is_existing:
        existing = True
    else:
        existing = sociallogin.lookup()

    if user.profile.should_gauntlet:
        request.session['gauntlet_redirect'] = True

    if user and not existing:
        sociallogin.connect(request, user)


@receiver(user_signed_up)
def handle_signup(request, user, sociallogin=None, **kwargs):
    with transaction.atomic():
        full_un = user.first_name + ' ' + user.last_name
        user.username = full_un
        user.save()
        profile = Profile()
        profile.name = full_un
        profile.user = user
        profile.save()

        if sociallogin and sociallogin.account.provider == 'facebook':
            if sociallogin.account.extra_data['gender'] == 'male':
                profile.gender = profile_models.GENDER_MALE
            elif sociallogin.account.extra_data['gender'] == 'female':
                profile.gender = profile_models.GENDER_FEMALE

            handle_avatar(profile, sociallogin.account)

            profile.save()

        wh.set_wedge_egilibility(request, True, sociallogin.account)


@receiver(post_save, sender=Stance)
def handle_mention_save_stance(sender, instance, created, **kwargs):
    if created:
        mention(instance.stance_text, mentioner=instance.user, stance=instance, stance_comment=None)


@receiver(user_logged_in)
def logged_in(sender, user, request, **kwargs):
    pass