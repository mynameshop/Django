from __future__ import unicode_literals

import reversion
from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

class QuestionManagerBase(models.Manager):
    def filter(self, *args, **kwargs):
        if 'slug' in kwargs:
            # Needed in order to facilitate case insensitive validation everywhere
            kwargs['slug__iexact'] = kwargs['slug']
            del kwargs['slug']
        return super(QuestionManagerBase, self).filter(*args, **kwargs)


class AnswerManager(models.Manager):
    def filter_list_prefetch(self, *args, **kwargs):
        filtered_data = self.filter(*args, **kwargs)
        return filtered_data.prefetch_related('stance', 'stance__question', 'stance__user', 'user')


@reversion.register()
class Answer(TimeStampedModel):
    objects = AnswerManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stance = models.ForeignKey('stances.Stance', on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name="answers")

    class Meta:
        unique_together = ('question', 'user',)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.stance and self.stance.question:
            self.question = self.stance.question

        super(Answer, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '{} {}'.format(self.id, self.user)


class QuestionManager(QuestionManagerBase):
    def mark_choices(self, questions, user):
        if user and not user.is_anonymous():
            for question in questions:
                answer = question.get_user_answer(user)
                question.user_choice = question.get_user_choice(user, answer)
                if answer and answer.stance:
                    question.user_stance = answer.stance.stance_text
                    question.answer = answer


class Question(TimeStampedModel):
    objects = QuestionManager()

    slug = models.SlugField(unique=True)
    question = models.TextField()
    statement = models.TextField()
    details = models.TextField()
    even_more = models.TextField(default="Coming soon")
    pro_label = models.CharField(max_length=250, default="For")
    con_label = models.CharField(max_length=250, default="Against")
    na_label = models.CharField(max_length=250, default="Not available")
    num_pro_votes = models.PositiveIntegerField(default=0)
    num_con_votes = models.PositiveIntegerField(default=0)
    num_na_votes = models.PositiveIntegerField(default=0)
    num_total_votes = models.PositiveIntegerField(default=0)

    def count_votes(self, choice):
        return Answer.objects.filter(stance__question=self, stance__choice=choice).count()

    def update_votes(self):
        # Use this to update counts on changes.  Instead of generating counts on the fly and caching
        # TODO: I don't think this is accurate. It counts all rows in the answer
        # table, but users have answer history in here.  so it needs to counts
        # distinct on user?
        self.num_pro_votes = Answer.objects.filter(stance__question=self, stance__choice='p').count()
        self.num_con_votes = Answer.objects.filter(stance__question=self, stance__choice='c').count()
        self.num_na_votes = Answer.objects.filter(stance__question=self, stance__choice='u').count()
        self.num_total_votes = self.num_pro_votes + self.num_con_votes + self.num_na_votes
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return 'questions:question', (), {"slug": self.slug}

    @property
    def pro_percentage(self):
        pro_percentage = 0
        if self.num_total_votes != 0:
            pro_percentage = (self.num_pro_votes * 100) / self.num_total_votes
        return pro_percentage

    @property
    def con_percentage(self):
        con_percentage = 0
        if self.num_total_votes != 0:
            con_percentage = (self.num_con_votes * 100) / self.num_total_votes
        return con_percentage

    @property
    def na_percentage(self):
        na_percentage = 0
        if self.num_total_votes != 0:
            na_percentage = (self.num_na_votes * 100) / self.num_total_votes
        return na_percentage

    def get_user_answer(self, user):
        if user and not user.is_anonymous():
            try:
                answer = Answer.objects.filter(stance__question=self, user=user).last()
                return answer
            except Answer.DoesNotExist:
                return None
        else:
            return None

    def get_user_choice(self, user, answer=None):
        if answer is None:
            answer = self.get_user_answer(user)

        if answer is not None:
            return answer.stance.choice
        else:
            return None

    def get_user_stance(self, user, answer=None):
        if answer is None:
            answer = self.get_user_answer(user)

        if answer is not None:
            return answer.stance
        else:
            return None

    def __str__(self):
        return self.slug


class SuggestedQuestionManager(QuestionManagerBase):
    pass


class SuggestedQuestion(TimeStampedModel):
    objects = SuggestedQuestionManager()

    slug = models.SlugField(unique=True)
    details = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True)
    related_question = models.ForeignKey(Question,
                                         verbose_name='Approved to question', default=None, null=True, blank=True)

    def is_approved_human_readable(self):
        if self.is_approved():
            return 'yes'
        else:
            return 'no'

    is_approved_human_readable.short_description = "Approved"

    def is_approved(self):
        return self.related_question is not None

    def get_username(self):
        if self.user is not None:
            username = self.user.username
        else:
            username = 'Anonymous'

        return username

    get_username.short_description = "User"

    def __str__(self):
        return '{}: {}'.format(self.get_username(), self.slug)
