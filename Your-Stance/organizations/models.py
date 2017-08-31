from model_utils.models import TimeStampedModel
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Organization(TimeStampedModel):
    """
       Proxy Profile

       Users can create multiple proxy profiles.  These are profiles of famous
       people or historical figures. Examples:  Benjamin Franklin, Adolf Hitler,
       Mother Teresa, Vincent van Gough, Taylor Swift, Oprah Winfrey, Michael
       Jordan, etc.

       """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    details = models.CharField(max_length=255, blank=True)
    num_members = models.PositiveIntegerField(default=0)
    is_manual = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name

