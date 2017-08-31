from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from profiles.models import Profile
from questions.models import Answer
from badges import helper as bh
from badges.models import Badge

@receiver(post_save, sender=Profile)
def user_save_callback(instance, sender, created, *args, **kwargs):
    if created:
        bh.give_badge(instance, Badge.TYPE_PIONEER)


@receiver(post_save, sender=Answer)        
def answer_save_callback(instance, sender, created, *args, **kwargs):
    bh.give_badge(instance.stance.user.profile, Badge.TYPE_GURU, answer=instance)