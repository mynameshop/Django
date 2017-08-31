import copy
from django.db.models import Q
from django.contrib.auth.models import User
from questions.models import Answer
from profiles.models import Profile

def move_base_to_front(base_user_pk, users, profiles):

    for u in users:
        u['base'] = False
        if u['user__pk'] == base_user_pk:
            users.insert(0, users.pop())
            u['base'] = True
            profiles.insert(0, profiles.pop())


    return (users, profiles)

def swap(users, profiles, from_i, to_i):
    users[to_i], users[from_i] = users[from_i], users[to_i]
    profiles[to_i], profiles[from_i] = profiles[from_i], profiles[to_i]

def reorder(base_user_pk, users, profiles, users_pks):
    current_i = 0

    users_pks = [int(u) for u in users_pks]

    for u in users:
        if u['user__pk'] != base_user_pk:
            i = users_pks.index(int(u['user__pk']))+1
            swap(users,profiles,current_i, i)

        current_i+=1

    return (users, profiles)


def get_user(user_pk):
    profiles =  Profile.objects.filter(Q(user__pk=user_pk))
    users = profiles.values('user__pk', 'user__username', 'user__profile__pk')
    user = users.first()
    user['avatar'] = profiles.first().thumb50.url

    return user

def comparison_data(base_user, users_pks, more, randomize_second=False):
    if randomize_second:
        user = User.objects.filter(profile__is_proxy=True).order_by('?').first()
        if user:
            users_pks = [user.pk, ]
    result = {}
    base_answers = Answer.objects.filter(user=base_user) #.order_by('-modified') #
    question_pks = base_answers.values_list('stance__question__pk', flat=True)
    user_answers = Answer.objects.filter(Q(stance__question__pk__in=question_pks)
        &
        (Q(user__in=users_pks)| Q(user=base_user))
        )



    profiles =  Profile.objects.filter(Q(user=base_user) | Q(user__pk__in=users_pks))
    users = profiles.values('user__pk', 'user__username', 'user__profile__pk')

    grouped = {}
    questions = base_answers.distinct('stance__question').values('stance__question__pk', 'stance__question__slug', 'stance__question__question')
    result['total_questions'] = len(questions)
    if more:
        limit_start = 0
        limit_count = result['total_questions']
    else:
        limit_start  = 0
        limit_count = 5

    questions = questions[limit_start:limit_count]
    comparison = user_answers.values('stance__question__pk', 'user__pk', 'stance__choice', 'stance__question__slug','modified').order_by('-modified')



    i = 0
    for p in users:
        p['avatar'] = profiles[i].thumb50.url
        i+=1

    profiles = list(profiles)
    users = list(users)
    users, profiles= move_base_to_front(base_user.pk, users, profiles)
    users, profiles = reorder(base_user.pk, users, profiles, users_pks)
    for c in questions:

        if 'stance__question__pk' not in grouped:
            grouped[c['stance__question__pk']] = {}

        if 'user__pk' not in grouped[c['stance__question__pk']]:
            for u in users:
                grouped[c['stance__question__pk']][u['user__pk']] = None


    for c in comparison:
        try:
            if grouped[c['stance__question__pk']][c['user__pk']] is None:
                grouped[c['stance__question__pk']][c['user__pk']] = c
        except KeyError:
            pass


    result['grouped'] = grouped
    result['users'] = users
    result['questions'] = questions



    return result
