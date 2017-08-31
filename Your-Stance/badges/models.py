from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel
 
class Badge(models.Model):
    TYPE_BRAVE = 'brave'
    TYPE_GURU = 'guru'
    TYPE_PIONEER = 'pioneer'
    TYPE_TEST = 'test'
    TYPE_CHOICES = [
        (TYPE_BRAVE, 'Brave (not implemented)'),
        (TYPE_GURU, 'Guru'),
        (TYPE_PIONEER, 'Pioneer'),
    ]
    PIONEER_THRESHOLD = 1000
    GURU_THRESHOLD = 100
    title = models.CharField(max_length=128)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, unique=True)
    details = models.TextField(blank=True, null=True)
    
    def get_image_fn(self):
        if self.type == Badge.TYPE_PIONEER:
            return 'pioneer.png'
        elif self.type == Badge.TYPE_GURU:
            return 'guru.png'
        else:
            return 'dummy.png'
    
    def __str__(self):
        return self.title
    
    
class ProfileBadge(TimeStampedModel):
    class Meta:
        unique_together = ['badge', 'profile']
    
    badge = models.ForeignKey("badges.Badge")
    profile = models.ForeignKey("profiles.Profile")