from __future__ import unicode_literals
from model_utils.models import TimeStampedModel

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from questions.models import Question
from profiles.mentions import mention
import notifications.models as nmodels
from notifications import helper as nh

class Forum(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    details = models.CharField(max_length=250)
    priority = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Thread(TimeStampedModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    num_comments = models.PositiveIntegerField(default=1)
    last_comment = models.ForeignKey("Comment", on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='+')

    def __str__(self):
        return self.title

    def count_comments(self):
        self.num_comments = Comment.objects.filter(topic_id=self).count()
        self.save()



class Comment(TimeStampedModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text


@receiver(post_save, sender=Comment)
def handle_save_comment(sender, instance, created, **kwargs):

    if created:

        mention(
            instance.comment_text,
            mentioner=instance.author,
            notification_type=nmodels.FORUM_MENTION,
            comment=instance
        )

        involved = Comment.objects.filter(thread=instance.thread).distinct('author')


        for inv in involved:

            if inv.author == instance.author:
                continue

            nh.send_notification(user_to=inv.author, user_from=instance.author, type=nmodels.REPLY_FORUM_COMMENT, comment=instance)
