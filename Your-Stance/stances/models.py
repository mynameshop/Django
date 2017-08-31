from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from model_utils.models import TimeStampedModel
from questions.models import Answer


class StanceManager(models.Manager):
    def top10(self, question_id):
        top = self.filter_counts_and_order(question=question_id)[:10]

        i = 1
        for t in top:
            t.rank = i
            i += 1

        return top

    def filter_counts_and_order(self, reverse=True, *args, **kwargs):
        with_counts = self.filter_with_counts(*args, **kwargs)
        result = sorted(with_counts, key=lambda t: t.adherent_count, reverse=reverse)
        return result

    def filter_with_counts(self, *args, **kwargs):
        filtered = self.filter(*args, **kwargs)
        for f in filtered:
            f.adherent_count = f.get_adherent_count()
        return filtered

    def filter_with_stars(self, user, *args, **kwargs):
        filtered = self.filter(*args, **kwargs)
        q = Q(stance__in=filtered)

        if user.is_authenticated():
            q &= Q(user=user)

        stars = Star.objects.filter(q).select_related('stance') \
            .values_list('stance__pk', flat=True)

        return (filtered, stars)

    def filter_listprefetch(self, *args, **kwargs):
        filtered_data = self.filter(*args, **kwargs)

        return filtered_data. \
            prefetch_related('question', 'user', 'user__profile')


class Stance(TimeStampedModel):
    objects = StanceManager()

    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=settings.QUESTION_CHOICES,
                              null=True, default='p')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stance_text = models.TextField(null=True, blank=True)
    citation = models.TextField(null=True, blank=True)
    stamp = models.DateField(verbose_name="Timestamp", null=True, blank=True)
    root = models.ForeignKey('self', null=True, blank=True, related_name='stanceroot')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='stanceparent')
    round = models.PositiveIntegerField(default=1)
    num_comments = models.PositiveIntegerField(default=0)
    num_stars = models.PositiveIntegerField(default=0)
    num_agree = models.PositiveIntegerField(default=0)

    def get_adherent_answers_qs(self):
        answers = Answer.objects.filter(Q(stance=self) & ~Q(user=self.user)).distinct('user')
        processed_answers = []

        for a in answers:
            got_answers = Answer.objects.filter(Q(user=a.user)
                                                & Q(stance__question=self.question) & ~Q(stance=self)
                                                & Q(modified__gt=a.modified)).order_by('-modified')

            if len(got_answers) == 0:
                processed_answers.append(a)

        return processed_answers

    def get_adherent_answers(self):
        return self.get_adherent_answers_qs()[:5]

    def get_adherent_count(self):
        return len(self.get_adherent_answers_qs())

    def get_stars(self):
        return Star.objects.filter(stance=self)

    def count_stars(self):
        return len(self.get_stars())

    def get_children(self, distinct_user=False, exclude_user_pks=[]):
        stances = Stance.objects.filter(Q(Q(root=self) | Q(pk=self.pk)) & ~Q(user__pk__in=exclude_user_pks))
        if distinct_user:
            stances = stances.distinct('user')
        return stances

    get_adherent_count.short_description = "Num. adherents"

    def __str__(self):
        # return '{}'.format(self.stance_text[:60]).encode('utf-8')
        return '%s %s' % (self.user, self.created)


class Star(TimeStampedModel):
    stance = models.ForeignKey(Stance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
