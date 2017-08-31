from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from forums.models import Thread
from profiles.models import Follow
from questions.models import Question, Answer
from stances.models import Stance


# Home views
def stancelist_test(request):
    stances = Stance.objects.filter_listprefetch(~Q(choice='u')) \
                  .order_by('-created')[:50]

    return render(request, 'performance_test/stance_list.html', {
        'stances': stances})


def questionlist_test(request):
    questions = Question.objects.order_by('-created')  # [:10]
    return render(request, 'performance_test/question_list.html', {
        'questions': questions})


def userlist_test(request):
    users = User.objects.prefetch_related('profile').order_by('-date_joined')
    return render(request, 'performance_test/user_list.html', {
        'users': users})


def threadlist_test(request):
    threads = Thread.objects.order_by('-modified')

    return render(request, 'performance_test/thread_list.html', {
        'threads': threads})


# Profile views
def answerlist_test(request, username):
    user = User.objects.get(username__iexact=username)
    answers = Answer.objects.filter_list_prefetch(user=user).order_by('stance__question', '-modified').distinct(
        'stance__question')
    return render(request, 'performance_test/answer_list.html', {
        'answers': answers})


def follow_test(request, username):
    user = User.objects.get(username__iexact=username)
    follow = Follow.objects.get_usr_follow(followed_user=user, follower_user=request.user)
    followed = Follow.objects.find_followed(user)
    followers = Follow.objects.find_followers(user)
    return render(request, 'performance_test/follow.html', {
        'follow': follow})


def counters_test(request, username):
    user = User.objects.get(username__iexact=username)
    follow = Follow.objects.get_usr_follow(followed_user=user, follower_user=request.user)
    followed = Follow.objects.find_followed(user)
    followers = Follow.objects.find_followers(user)
    if follow is None:
        is_followed = False
    else:
        is_followed = True
    return render(request, 'performance_test/profile_counters.html', {
        'counter_questions':  user.profile.question_list_count,
        'counter_answers': user.profile.answered_questions_count,
        'counter_followed': len(followed),
        'counter_followers': len(followers),
        'is_followed': is_followed,
    })


# Misc
def middleware_test(request):
    return render(request, 'performance_test/base.html')
