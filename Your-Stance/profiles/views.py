from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from notifications import helper as nh
from notifications import models as nm
from profiles import comparison_helper as ch
from profiles import wedge_helper as wh
from profiles.forms import FbWedgeForm
from profiles.friendlist import FBFriendGetter, DummyFriendGetter, \
    GoogleFriendGetter, TwitterFriendGetter, send_invitation_email
from profiles.models import Follow, ProfileVerification
from questions.models import Answer
from stances.models import Stance


class ProfilesView(View):
    template_name = 'profiles/profiles.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.order_by('-date_joined')
        return render(request, self.template_name, {
            'users': users,
        })


class ProfileViewBase(View):
    def get(self, request, *args, **kwargs):
        self.username = self.kwargs['username']
        try:
            self.user = User.objects.prefetch_related('profile').get(username__iexact=self.username)
        except ObjectDoesNotExist as e:
            raise Http404("user not found")
        self.answers = Answer.objects.filter_list_prefetch(user=self.user).order_by('stance__question',
                                                                                    '-modified').distinct(
            'stance__question')
        self.stances = Stance.objects.filter_listprefetch(user=self.user)
        self.is_followed = False
        if request.user.is_authenticated():
            if request.user != self.user:
                follow = Follow.objects.get_usr_follow(followed_user=self.user, follower_user=request.user)
                if follow is None:
                    self.is_followed = False
                else:
                    self.is_followed = True
            else:
                self.is_followed = False

        self.followed = Follow.objects.find_followed(self.user)
        self.followers = Follow.objects.find_followers(self.user)
        self.followed_count = self.followed.count()
        self.follower_count = self.followers.count()

    def add_counters(self, context_dict):
        context_dict.update({
            'counter_questions': self.user.profile.question_list_count,
            'counter_answers': self.user.profile.answered_questions_count,
            'counter_followed': self.followed_count,
            'counter_followers': self.follower_count,
            'is_followed': self.is_followed,
            'answers': self.answers,
            'user': self.user,
        })
        return context_dict


def comparsion_ajax(request):
    type = request.GET.get('type', 'comparision')
    more = bool(int(request.GET.get('more', False)))
    user_pks = request.GET.getlist('user_pk[]')
    base_user_pk = request.GET.get('base_user_pk')
    base_user = User.objects.get(pk=base_user_pk)
    comparison_data = ch.comparison_data(base_user, user_pks, more)

    if type == 'comparision':
        return render(request, 'profiles/profile_sheet_inner.html', {
            'comparison_data': comparison_data,
        })
    else:
        return render(request, 'profiles/profile_sheet.html', {
            'comparison_data': comparison_data,
            'max_comparison': ProfileView.MAX_COMPARISON,
            'more': int(more),
        })


class ProfileView(ProfileViewBase):
    template_name = 'profiles/profile.html'
    MAX_COMPARISON = 5

    def get(self, request, *args, **kwargs):
        super(ProfileView, self).get(request, *args, **kwargs)

        if self.request.user.is_authenticated():
            comparison_data = ch.comparison_data(self.user, [self.request.user.pk, ], False)
        else:
            comparison_data = ch.comparison_data(self.user, [], False, True)

        return render(request, self.template_name, self.add_counters({
            'user': self.user,
            'answers': self.answers,
            'heroes': self.followed[:5],
            'comparison_data': comparison_data,
            'stances': self.stances,
            'max_comparison': ProfileView.MAX_COMPARISON,
            'more': 0

        }))


class FollowersView(ProfileViewBase):
    template_name = 'profiles/followers.html'

    def get(self, request, *args, **kwargs):
        super(FollowersView, self).get(request, *args, **kwargs)

        return render(request, self.template_name, self.add_counters({
            'user': self.user,
            'followers': self.followers,
        }))


class FollowedView(ProfileViewBase):
    template_name = 'profiles/followed.html'

    def get(self, request, *args, **kwargs):
        super(FollowedView, self).get(request, *args, **kwargs)

        return render(request, self.template_name, self.add_counters({
            'user': self.user,
            'followed': self.followed,
        }))


class FacebookWedgeView(LoginRequiredMixin, View):
    template_name = 'profiles/wedge.html'

    def setup(self, post=None, files=None):
        initial = {
            'username': self.request.user.username,
            'display_name': self.request.user.profile.name,
        }
        if post:
            self.form = FbWedgeForm(post, files, initial=initial)
        else:
            self.form = FbWedgeForm(initial=initial)

        self.form.set_user(self.request.user)

    def post(self, request, *args, **kwargs):
        if not wh.is_wedge_eligible(request):
            return redirect('/')
        self.setup(request.POST, request.FILES)

        if self.form.is_valid():
            verification = self.request.user.profile.get_verification()

            if verification is None:
                verification = ProfileVerification()

            verification.status = ProfileVerification.STATUS_PENDING
            verification.photo = self.form.cleaned_data['verification']
            verification.user = self.request.user

            self.request.user.username = self.form.cleaned_data['username']
            self.request.user.profile.name = self.form.cleaned_data['display_name']
            user = self.request.user
            self.request.user.set_password(self.form.cleaned_data['password'])
            update_session_auth_hash(self.request, user)

            verification.save()
            self.request.user.save()
            self.request.user.profile.save()

            wh.set_wedge_egilibility(request, False)

            if user.profile.should_gauntlet:
                next_url = reverse('questions:gauntlet')
            else:
                next_url = self.request.session.pop(wh.NEXT_KEY, '/')

            return redirect(next_url)

        return render(request, self.template_name, {
            'form': self.form,
            'hide_gauntlet_warning': True,
        })

    def get(self, request, *args, **kwargs):
        if not wh.is_wedge_eligible(request):
            return redirect('/')
        self.setup()

        return render(request, self.template_name, {
            'form': self.form,
            'hide_gauntlet_warning': True,
        })


class FollowFriendsView(LoginRequiredMixin, View):
    template_name = 'profiles/follow_friends.html'

    def get(self, request, *args, **kwargs):
        selected_service = request.GET.get('service', 'fb')

        response = render(request, self.template_name, {
            'selected_service': selected_service,
        })
        response.set_cookie("follow_friends_redir", None)
        request.user.profile.follow_process_is_complete = True
        request.user.profile.save()
        return response


def friendlist_google_connect(request):
    response = redirect('/red/accounts/google/login/')
    response.set_cookie("follow_friends_redir", reverse('profiles:follow_friends') + "?service=gmail")
    return response


def friendlist_twitter_connect(request):
    response = redirect('/red/accounts/twitter/login/')
    response.set_cookie("follow_friends_redir", reverse('profiles:follow_friends') + "?service=twitter")
    return response


def friendlist_ajax(request):
    type = request.GET.get('type', 'test')

    if type == 'fb':
        getter = FBFriendGetter(request.user)
    elif type == 'gmail':
        getter = GoogleFriendGetter(request.user)
    elif type == 'twitter':
        getter = TwitterFriendGetter(request.user, request)
    else:
        getter = DummyFriendGetter(request.user)

    getter.set_paging_data({'max_res': request.GET.get('max_res'), 'next': request.GET.get('next')})
    is_connected = getter.is_connected()

    friends = []

    if is_connected:
        friends = getter.get_friends()

    return render(request, 'profiles/follow_friends_list.html', {
        'friends': friends,
        'service_name': getter.get_name(),
        'is_connected': is_connected,
        'next': getter.get_next(),
        'type': type,
    })


@csrf_exempt
def friendlist_invite_email_ajax(request):
    if not request.user.is_authenticated() or request.method != 'POST':
        return JsonResponse({'ok': False})

    email = send_invitation_email(request.user, request.POST.get('email'))

    return JsonResponse({'ok': True, 'email': email})


@csrf_exempt
def friendlist_invite_twitter_ajax(request):
    uid = request.POST.get('uid')
    getter = TwitterFriendGetter(request.user, request)
    api = getter.get_api()

    invitation_text = request.user.username + " invites you to Yourstance. You can join here http://www.yourstance.com/register/"
    api.PostDirectMessage(text=invitation_text, user_id=uid)

    return JsonResponse({'ok': True})


def mentions_ajax(request):
    username = request.GET.get('username', '')

    users = User.objects.filter(username__icontains=username).values_list('username', flat=True)

    return JsonResponse(list(users), safe=False)


def users_ajax(request):
    username = request.GET.get('username', '')

    users = User.objects.filter(username__icontains=username).values('username', 'id')

    if username == '':
        users = users[:10]

    if username == '':
        users = users[:10]

    return JsonResponse(list(users), safe=False)


@csrf_exempt
def follow_ajax(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({'ok': False, 'error': 'Not logged in'})

    followed = False
    followed_user = User.objects.get(username__iexact=username)
    follow_object = Follow.objects.get_usr_follow(followed_user, request.user)

    if followed_user == request.user:
        return JsonResponse({'ok': False, 'error': 'Self-follow'})

    if follow_object is not None:
        follow_object.delete()
        followed = False
    else:
        followed = True
        follow_object = Follow(followed=followed_user.profile, follower=request.user.profile)
        follow_object.save()
        if not request.user.profile.is_proxy:
            nh.send_notification(user_to=followed_user, user_from=request.user, type=nm.FOLLOWED)

    return JsonResponse({'ok': True, 'followed': followed})
