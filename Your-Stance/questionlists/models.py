from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

# from questions.models import Question
from profiles.models import Profile


class QuestionList(TimeStampedModel):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User)
    num_questions = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class QuestionListItem(models.Model):
    list = models.ForeignKey(QuestionList)
    question = models.ForeignKey('questions.Question')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.list:
            list = self.list
        else:
            list = ""
        if self.question:
            question = self.question
        else:
            question = ""
        
        return "%s %s %s" % (self.pk, question.slug, list)
