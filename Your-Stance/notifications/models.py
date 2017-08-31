from __future__ import unicode_literals
from model_utils.models import TimeStampedModel

from django.db import models
from django.contrib.auth.models import User



REPLY_STANCE_COMMENT = 'RS'
REPLY_FORUM_COMMENT = 'RF'
AGREE = 'AG'
LIKE = 'LI'
MENTION = 'MT'
FORUM_MENTION = 'FM'
FOLLOWED = 'FW'
NEW_QUESTION = 'NQ'

NOTIFICATION_TYPES = (
    (NEW_QUESTION, 'New question'),
    (REPLY_STANCE_COMMENT, 'Reply to stance comment'),
    (REPLY_FORUM_COMMENT, 'Reply to forum comment'),
    (AGREE, 'Agreed with your stance'),
    (LIKE, 'Liked your comment'),
    (MENTION, 'Mentioned your name'),
    (FORUM_MENTION, 'Mentioned you in forums'),
    (FOLLOWED, 'Followed by other user')
)


class Notification(TimeStampedModel):
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+',)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES, default=REPLY_STANCE_COMMENT)
    stance = models.ForeignKey("stances.Stance", on_delete=models.CASCADE, blank=True, null=True, default=None)
    comment = models.ForeignKey("forums.Comment", on_delete=models.CASCADE, blank=True, null=True, default=None)
    

#class UserEmailNotification(models.Model):
#    class Meta:
#        unique_together = ['user', 'type']
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
#    type = models.CharField(max_length=4, choices=NOTIFICATION_TYPES)