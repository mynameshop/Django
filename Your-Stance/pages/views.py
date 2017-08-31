from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from pages.forms import RegisterProfileForm
from profiles.models import Profile, ProfileVerification


class RulesView(View):
    template_name = 'pages/rules.html'

    def get(self, request):
        return render(request, self.template_name)


class TosView(View):
    template_name = 'pages/tos.html'

    def get(self, request):
        return render(request, self.template_name)


class WhatTheView(View):
    template_name = 'pages/what_the.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactView(View):
    template_name = 'pages/contact.html'

    def get(self, request):
        return render(request, self.template_name)


class PrivacyView(View):
    template_name = 'pages/privacy.html'

    def get(self, request):
        return render(request, self.template_name)


class FaqView(View):
    template_name = 'pages/faq.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'pages/login.html'

    def post(self, request):
        referer = request.session.get('referer', None)
        logout(request)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        error_message = None

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['referer'] = referer
                if user.profile.should_gauntlet:
                    return redirect(reverse('questions:gauntlet'))
                else:
                    return redirect(request.POST.get('next', '/'))
            else:
                error_message = 'This account is not active.'
        else:
            error_message = 'Email and password doesn\'t match.'

        return render(request, self.template_name, {
            'error_message': error_message,
            'next': request.POST.get('next')
        })

    def get(self, request):

        return render(request, self.template_name, {
            'next': request.GET.get('next')
        })


class RegisterView(View):
    template_name = 'pages/register.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')

        form = RegisterProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user = User(email=form.data['email'], username=form.data['username'], is_active=True)
            user.set_password(form.data['password'])
            user.save()

            profile = Profile(
                name=form.data['display_name'],
                birthday=form.cleaned_data['birthday'].strftime('%Y-%m-%d'),
                gender=form.data['gender'],
                avatar=request.FILES['avatar'],
                user=user,
                is_verified=False
            )
            profile.save()

            verification = ProfileVerification(user=user, status=ProfileVerification.STATUS_PENDING,
                                               photo=request.FILES['avatar'])
            verification.save()

            user = authenticate(email=form.data['email'], password=form.data['password'])
            login(request, user)
            if user.profile.should_gauntlet:
                return redirect(reverse('questions:gauntlet'))
            else:
                return redirect(reverse('profiles:profile', kwargs={'username': user.username}))

        return render(request, self.template_name, {
            'form': form,
        })

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = RegisterProfileForm()
        return render(request, self.template_name, {
            'form': form,
        })


class FinishView(View):
    template_name = 'pages/finish.html'

    def get(self, request):
        return render(request, self.template_name)
