import math

from django.db.models import Q, F
from forums.models import Thread, Comment
from questions.models import Answer
from stances.models import Stance

FEED_LIMIT = 30


def add_to_merged(queryset, merged, type):
    for x in queryset:
        x.type = type
        merged.append(x)


def reorder_merged(merged):
    merged.sort(key=lambda x: x.created, reverse=True)


def compile_feed(start, count):
    div_count = math.ceil(count / 4)

    stances = Stance.objects.filter_listprefetch(~Q(choice='u')).order_by('-created')[start:div_count + start]
    threads = Thread.objects.prefetch_related('author', 'author__profile', 'question') \
                  .order_by('-created')[start:div_count + start]
    comments = Comment.objects.prefetch_related('author', 'author__profile', 'thread', 'thread__question') \
                   .order_by('-created')[start:div_count + start]
    agrees = Answer.objects \
                 .prefetch_related('stance', 'question', 'user', 'user__profile', 'stance__user',
                                   'stance__user__profile') \
                 .filter(~Q(user=F('stance__user'))).order_by('-created')[start:div_count + start]

    # sum_length = len(stances)+len(threads)+len(comments)
    merged = []

    add_to_merged(stances, merged, 'stance')
    add_to_merged(threads, merged, 'thread')
    add_to_merged(comments, merged, 'comment')
    add_to_merged(agrees, merged, 'agree')
    merged = merged  # [start:count+start]

    reorder_merged(merged)

    # print "LENGTH", len(merged)


    return merged
