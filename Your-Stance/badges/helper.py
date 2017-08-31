from django.db.models import Q
from django.contrib.auth.models import User

from profiles.models import Profile
from badges.models import Badge, ProfileBadge
from stances.models import Stance


def user_has_badge(profile, badge_type):
    if len(ProfileBadge.objects.filter(profile=profile, badge__type=badge_type)) == 0:
        return False
    else:
        return True

def is_guru_eligible(profile, answer):

    if answer is None:
        stances = Stance.objects.filter(user=profile.user)
        for stance in stances:
            if stance.num_agree()>=Badge.GURU_THRESHOLD:
                return True
        return False

    eligible_user = answer.stance.user
    adherent_count = len(answer.stance.get_adherent_answers_qs())

    if adherent_count>=Badge.GURU_THRESHOLD:
        return True
    else:
        return False


def is_badge_eligible(profile, badge, **kwargs):
    if badge.type == Badge.TYPE_PIONEER:
        existing_profiles = Profile.objects.filter(~Q(user=None) & Q(is_proxy=False))
        if len(existing_profiles)<=Badge.PIONEER_THRESHOLD and Badge.PIONEER_THRESHOLD != -1:
            return True
        else:
            return False
    elif badge.type == Badge.TYPE_GURU:
        return is_guru_eligible(profile, kwargs.get('answer'))
    elif badge.type == Badge.TYPE_TEST:
        return True

    return False


def give_badge(profile, badge_type, **kwargs):
    try:
        badge = Badge.objects.get(type=badge_type)
    except Badge.DoesNotExist:
        return
    if user_has_badge(profile, badge_type):
        return
    if is_badge_eligible(profile, badge, **kwargs):
        ProfileBadge(profile=profile, badge=badge).save()


def revoke_badge(profile, badge_type):
    try:
        profile_badge = ProfileBadge.objects.get(profile=profile, badge__type=badge_type)
    except ProfileBadge.DoesNotExist:
        return

    profile_badge.remove()


def get_profile_badges(profile):
    """
    Maybe its a bit overkill. But just in case of additional logic.
    """
    return ProfileBadge.objects.filter(profile=profile)

def sync_badges(profile):

    badges = Badge.objects.all()

    for badge in badges:
        eligible = is_badge_eligible(profile, badge)
        has_badge = user_has_badge(profile, badge.type)

        if eligible and not has_badge:
            give_badge(profile, badge.type)
