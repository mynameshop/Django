from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ImageUploadForm, EditProfileForm, NotificationsForm, VerificationForm
from profiles.models import Profile, ProfileVerification
from badges import helper as bh


class ProfileView(LoginRequiredMixin, View):
    template_name = 'user_settings/profile.html'

    def get(self, request):
        u = request.user
        data = {'username': u.username,
                'name': u.profile.name,
                'email': u.email,
                'location': u.profile.location,
                'bio': u.profile.bio
                }
        form = EditProfileForm(initial=data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            u = User.objects.get(pk=request.user.id)
            u.username = form.cleaned_data['username']
            u.email = form.cleaned_data['email']
            u.save()
            p = Profile.objects.get(pk=request.user.profile.id)
            p.name = form.cleaned_data['name']
            p.location = form.cleaned_data['location']
            p.bio = form.cleaned_data['bio']
            p.save()
            return HttpResponseRedirect(reverse('settings:profile'))
        return render(request, self.template_name, {'form': form})


class AccountView(LoginRequiredMixin, View):
    template_name = 'user_settings/account.html'

    def get(self, request):
        return render(request, self.template_name, {})


class NotificationsView(LoginRequiredMixin, View):
    template_name = 'user_settings/notifications.html'

    def get(self, request):
        u = request.user
        data = {'question': u.profile.notification_question,
                'follower': u.profile.notification_follower,
                'agrees': u.profile.notification_agrees,
                'comment': u.profile.notification_comment,
                'mention': u.profile.notification_mention,
                'like': u.profile.notification_like

                }

        form = NotificationsForm(initial=data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = NotificationsForm(request.POST)

        if form.is_valid():
            p = Profile.objects.get(pk=request.user.profile.id)
            p.notification_question = form.cleaned_data['question']
            p.notification_follower = form.cleaned_data['follower']
            p.notification_agrees = form.cleaned_data['agrees']
            p.notification_comment = form.cleaned_data['comment']
            p.notification_mention = form.cleaned_data['mention']
            p.notification_like = form.cleaned_data['like']
            p.save()
            return HttpResponseRedirect(reverse('settings:notifications'))
        # return render(request, self.template_name, {'form': form})
        print form.cleaned_data['replies']
        return HttpResponseRedirect(reverse('home'))


class SettingsBadgesView(LoginRequiredMixin, View):
    template_name = 'user_settings/badges.html'

    def get(self, request):
        user_badges = bh.get_profile_badges(request.user.profile)
        return render(request, self.template_name, {
            'user_badges': user_badges,
        })


class SettingsOrganizationsView(LoginRequiredMixin, View):
    template_name = 'user_settings/organizations.html'

    def get(self, request):
        return render(request, self.template_name, {})


class VerificationView(LoginRequiredMixin, View):
    template_name = 'user_settings/verification.html'
    
    def add_context(self, context_dict):
        context_dict.update({
            'verification': self.verification,
            'form': self.form,
        })
        return context_dict
    
    def prepare(self, post=None, files=None):
        self.verification = self.request.user.profile.get_verification()
        if post:
            if self.verification is None:
                self.verification = ProfileVerification(user=self.request.user)
            self.form = VerificationForm(post, files, instance=self.verification)
        else:
            self.form = VerificationForm(instance=self.verification)
            
    def post(self, request):
        self.prepare(request.POST, request.FILES)
        if self.form.is_valid():
            self.form.save()
            return HttpResponseRedirect(reverse('settings:verification'))
        else:
            return render(request, self.template_name, self.add_context({}))
    
    def get(self, request):
        self.prepare()
        return render(request, self.template_name, self.add_context({}))


def upload_avatar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            p = Profile.objects.get(pk=request.user.profile.id)
            p.avatar = form.cleaned_data['image']
            p.save()
            return HttpResponseRedirect(reverse('settings:profile'))
    return HttpResponseRedirect(reverse('home'))


