import uuid

from datetime import date

import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel
from notifications.models import Notification
from questions.models import Question, Answer

# from stances.models

GENDER_MALE = 'm'
GENDER_FEMALE = 'f'
GENDER_CHOICES = (
    (GENDER_MALE, 'male'),
    (GENDER_FEMALE, 'female'),
)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars', filename)


def get_verify_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('verification', filename)


class FollowManager(models.Manager):
    def get_usr_follow(self, followed_user, follower_user):

        try:
            follow_object = self.get(followed=followed_user.profile, follower=follower_user.profile)
        except Follow.DoesNotExist:
            follow_object = None

        return follow_object

    def find_followers(self, user):
        return self.prefetch_related('follower', 'follower__user').filter(followed=user.profile)

    def find_followed(self, user):
        return self.prefetch_related('followed', 'followed__user').filter(follower=user.profile)


class Follow(models.Model):
    class Meta:
        unique_together = ['follower', 'followed']

    objects = FollowManager()

    follower = models.ForeignKey("profiles.Profile", related_name="follower")
    followed = models.ForeignKey("profiles.Profile", related_name="followed")

    def __str__(self):
        return "%s -> %s (%s)" % (self.follower.user.username, self.followed.user.username, self.pk)


class ProfileVerificationManager(models.Manager):
    def get_if_exists(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None


class ProfileVerification(TimeStampedModel):
    """
    When user applies for verification, this model is used.
    """

    objects = ProfileVerificationManager()

    class Meta:
        unique_together = ['user', ]
        verbose_name = 'Profile verification'
        verbose_name_plural = 'Profile verification'

    STATUS_PENDING = 'p'
    STATUS_VERIFIED = 'f'
    STATUS_REJECTED = 'r'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'pending'),
        (STATUS_VERIFIED, 'verified'),
        (STATUS_REJECTED, 'rejected'),
    )
    user = models.ForeignKey(User)
    photo = models.ImageField(upload_to=get_verify_path, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    thumb50 = ImageSpecField(source='photo',
                             processors=[ResizeToFill(50, 50)],
                             format='JPEG',
                             options={'quality': 80})
    thumb100 = ImageSpecField(source='photo',
                              processors=[ResizeToFill(100, 100)],
                              format='JPEG',
                              options={'quality': 80})
    thumb200 = ImageSpecField(source='photo',
                              processors=[ResizeToFill(200, 200)],
                              format='JPEG',
                              options={'quality': 80})

    def __str__(self):
        return "%s %s (%s)" % (self.user, self.get_status_display(), self.pk)


class Profile(TimeStampedModel):
    """
    Base profile class for the 3 profile types (Personal, Proxy, Party)

    """
    name = models.CharField(max_length=100)
    headline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=get_file_path)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    location = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(null=True, blank=True)
    deathhday = models.DateField(null=True, blank=True)
    old_birthday = models.CharField(max_length=50, blank=True)
    old_deathday = models.CharField(max_length=50, blank=True)
    is_proxy = models.BooleanField(default=False)
    is_famous = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    follow_process_is_complete = models.BooleanField(default=False)

    notification_question = models.BooleanField(default=True)
    notification_follower = models.BooleanField(default=True)
    notification_agrees = models.BooleanField(default=True)
    notification_comment = models.BooleanField(default=True)
    notification_like = models.BooleanField(default=True)

    notification_mention = models.BooleanField(default=True)

    thumb50 = ImageSpecField(source='avatar',
                             processors=[ResizeToFill(50, 50)],
                             format='JPEG',
                             options={'quality': 80})
    thumb100 = ImageSpecField(source='avatar',
                              processors=[ResizeToFill(100, 100)],
                              format='JPEG',
                              options={'quality': 80})
    thumb200 = ImageSpecField(source='avatar',
                              processors=[ResizeToFill(200, 200)],
                              format='JPEG',
                              options={'quality': 80})

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.questions_base_query = Question.objects

    @cached_property
    def question_list(self):
        return Question.objects.all()

    @cached_property
    def answered_questions(self):
        return self.questions_base_query.filter(answers__user=self.user).all()

    @cached_property
    def unanswered_questions(self):
        return self.questions_base_query.filter(~Q(answers__user=self.user)).all()

    @cached_property
    def unanswered_questions_plus_skipped(self):
        unanswered = [obj.pk for obj in self.unanswered_questions]
        skipped = [obj.pk for obj in self.skipped_questions]
        skipped += unanswered
        return self.questions_base_query.filter(pk__in=unanswered).all()

    @cached_property
    def skipped_questions(self):
        return self.answered_questions.filter(answers__stance__choice=settings.UNSURE).all()

    @property
    def age(self):
        if self.birthday is None:
            return None
        today = date.today()
        return (today.year - self.birthday.year - ((today.month, today.day) <
                                                   (self.birthday.month, self.birthday.day)))

    def __str__(self):
        return self.name

    @property
    def unread_notif_count(self):
        return Notification.objects.filter(user_to=self.user, is_read=False).count()

    @property
    def total_notif_count(self):
        return Notification.objects.filter(user_to=self.user, is_read=False).count()

    def read_all_notifs(self):
        return Notification.objects.filter(user_to=self.user, is_read=False).update(is_read=True)

    @cached_property
    def answered_questions_count(self):
        return len(self.answered_questions)

    @cached_property
    def question_list_count(self):
        return len(self.question_list)

    @cached_property
    def should_gauntlet(self):
        return self.answered_questions_count < self.question_list_count

    @cached_property
    def unanswered_questions_count(self):
        return len(self.unanswered_questions)

    def get_verification(self):
        return ProfileVerification.objects.get_if_exists(user=self.user)


@receiver(post_save, sender=ProfileVerification)
def verification_post_save_handler(sender, instance, **kwargs):
    if instance.status == ProfileVerification.STATUS_VERIFIED:
        instance.user.profile.is_verified = True
    else:
        instance.user.profile.is_verified = False
    instance.user.profile.save()
