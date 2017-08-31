from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from notifications import helper as nh
from notifications import models as nbmodels
from profiles.views import ProfileViewBase
from questions.models import Answer, Question
from yourstance.utils import append_next
from .forms import NewStanceForm, ReplyStanceForm, EditStanceForm
from .models import Stance, Star
import reversion


class StanceView(ProfileViewBase):
    template_name = 'stances/stance.html'

    def get(self, request, *args, **kwargs):
        super(StanceView, self).get(request, *args, **kwargs)
        if 'stance_id' in kwargs:
            stance_id = self.kwargs['stance_id']
        else:
            question = Question.objects.get(slug__iexact=self.kwargs['question_slug'])
            user = User.objects.get(username__iexact=self.kwargs['username'])
            answer = Answer.objects.filter(stance__question=question, user=user).last()
            stance_id = answer.stance.id
        root_id = stance_id
        stance = Stance.objects.get(pk=stance_id)
        if stance.parent:
            root_id = stance.root.id

        stances, stars = Stance.objects.filter_with_stars(request.user, Q(root=root_id) | Q(pk=root_id))

        return render(request, self.template_name,
                      self.add_counters({
                          'stances': stances,
                          'stance': stance,
                          'stars': stars,
                      })
                      )


class EditStanceView(LoginRequiredMixin, View):
    template_name = 'stances/edit.html'

    def check_stance_ownership(self, user, stance):
        if stance.user != user:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):

        stance = Stance.objects.get(pk=kwargs.get('stance_id'))
        self.check_stance_ownership(request.user, stance)
        form = EditStanceForm(request.POST, instance=stance)

        if form.is_valid():
            form.save()
            return redirect(reverse('stances:stance_edit', kwargs={'stance_id': stance.pk}))

        return render(request, self.template_name, {
            'form': form,
            'stance': stance,
        })

    def get(self, request, *args, **kwargs):

        stance = Stance.objects.get(pk=kwargs.get('stance_id'))
        self.check_stance_ownership(request.user, stance)
        form = EditStanceForm(instance=stance)
        return render(request, self.template_name, {
            'form': form,
            'stance': stance,
        })


class NewStanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = NewStanceForm(request.POST)
        new_stance = form.save(commit=False)
        if form.is_valid():
            with reversion.create_revision():
                new_stance.user = request.user
                choice = request.POST.get('choice', False)
                if choice:
                    new_stance.choice = choice
                new_stance.save()
                answer = Answer.objects.filter(user=request.user, question=new_stance.question).first()
                if not answer:
                    answer = Answer(user=request.user, question=new_stance.question)
                answer.stance = new_stance
                answer.save()
                n = int(request.POST.get('n', 0))
                if n == 1:
                    request.session["last_stance_id"] = answer.stance.id
                    return HttpResponseRedirect(reverse('questions:gauntlet'))
                    # request.session["last_stance_id"] = new_stance.id
                    # question = get_next_question()
                    # return HttpResponseRedirect(reverse('questions:question', args=[question.slug]))
        return HttpResponseRedirect(reverse('questions:question', args=[new_stance.question.slug]))


class ReplyStanceView(LoginRequiredMixin, View):
    template_name = 'stances/reply.html'

    def get(self, request, *args, **kwargs):
        stance_id = self.kwargs['stance_id']
        parent = Stance.objects.get(pk=stance_id)
        form = ReplyStanceForm()
        return render(request, self.template_name, {
            'form': form,
            'parent': parent
        })

    def post(self, request, *args, **kwargs):
        form = ReplyStanceForm(request.POST)
        if form.is_valid():
            stance_id = self.kwargs['stance_id']
            parent = Stance.objects.get(pk=stance_id)
            reply = form.save(commit=False)
            # Increase counts up the tree
            try:
                answer = Answer.objects.filter(stance__question=parent.question, user=request.user).latest('id')
            except ObjectDoesNotExist:
                answer = None
            if answer:
                reply.choice = answer.stance.choice
            reply.user = request.user
            reply.parent = parent
            if not parent.parent:
                parent.root = parent
            reply.root = parent.root
            reply.question = parent.question
            reply.save()

            children = reply.root.get_children(distinct_user=True, exclude_user_pks=[request.user.pk, ])

            for c in children:
                nh.send_notification(nbmodels.REPLY_STANCE_COMMENT,
                                     user_to=c.user, user_from=request.user,
                                     stance=parent)

        return HttpResponseRedirect(reverse('stances:stance',
                                            args=[parent.root.user.username,
                                                  parent.root.question.slug,
                                                  parent.root.id]))


def remove_stance(request, stance_id):
    current_stance = Stance.objects.get(pk=stance_id)
    blank_stance = Stance(question=current_stance.question,
                          choice=settings.UNSURE, user=request.user, stance_text='')
    blank_stance.save()
    answer = Answer(user=request.user, stance=blank_stance)
    answer.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def star_stance(request, stance_id):
    if not request.user.is_authenticated():
        request.session['referer'] = request.META.get('HTTP_REFERER')
        redir_url = append_next(reverse('pages:login'), reverse('stances:star', kwargs={'stance_id': stance_id}))
        return JsonResponse({
            'ok': False,
            'redir': redir_url
        })
    stance = get_object_or_404(Stance, pk=stance_id)
    try:
        old_star = Star.objects.filter(stance=stance, user=request.user).latest('id')
    except ObjectDoesNotExist:
        old_star = None
    if not old_star:
        star = Star()
        star.user = request.user
        star.stance = stance
        star.save()
        starred = True
        nh.send_notification(type=nbmodels.LIKE, user_to=stance.user, star=star)
    else:
        old_star.delete()
        starred = False
    stance.num_stars = stance.count_stars()
    stance.save()
    if request.is_ajax():
        return JsonResponse({
            'ok': True,
            'starred': starred,
            'num_stars': stance.num_stars,
        })
    else:
        return HttpResponseRedirect(request.session.pop('referer', '/'))


def select_stance(request):
    stance_id = request.GET.get('id')
    n = int(request.GET.get('n', 0))

    if not request.user.is_authenticated():
        request.session['referer'] = request.META.get('HTTP_REFERER')
        redir_url = append_next(reverse('pages:login'), reverse('stances:select'), {'id': stance_id, 'n': n})
        return HttpResponseRedirect(redir_url)

    stance = get_object_or_404(Stance, pk=stance_id)
    with reversion.create_revision():
        answer = Answer.objects.filter(user=request.user, question=stance.question).first()
        if answer is None:
            answer = Answer()
            answer.user = request.user
            answer.question = stance.question
        answer.stance = stance
        answer.save()

    stance.save()
    nh.send_notification(nbmodels.AGREE, user_to=stance.user, user_from=request.user, stance=stance)

    if n == 1:
        request.session["last_stance_id"] = stance.id
        return HttpResponseRedirect(reverse('questions:gauntlet'))

    return HttpResponseRedirect(request.session.pop('referer', request.META.get('HTTP_REFERER')))


def skip_stance(request):
    question = Question.objects.get(pk=request.GET.get('question_id'))
    stance = Stance()
    stance.question = question
    stance.user = request.user
    stance.choice = 'u'
    stance.stance_text = ""
    stance.save()
    answer = Answer()
    answer.user = request.user
    answer.stance = stance
    answer.save()
    return HttpResponseRedirect(reverse('questions:gauntlet'))


def stances_content(request):
    question = Question.objects.get(pk=request.GET.get('question_id'))
    sort_col = request.GET.get('sort_col')

    stances = Stance.objects.filter(question=question)

    if sort_col == 'random':
        stances = stances.order_by('?')
    elif sort_col == 'new':
        stances = stances.order_by('-created')
    elif sort_col == 'trending':
        stances = stances.order_by('-num_comments')
    elif sort_col == 'top':
        stances = Stance.objects.filter_counts_and_order(question=question)

    return render(request, 'stances/stances_content.html', {
        'stances': stances,
    })


def modal_content(request):
    question = Question.objects.get(pk=request.GET.get('question_id'))
    stances = Stance.objects.filter(question=question)

    return render(request, 'stances/select_stance_modal.html', {
        'question': question,
        'stances': stances,
    })


class CitationView(View):
    template_name = 'stances/citation.html'

    def get(self, request, *args, **kwargs):
        stance_id = kwargs.get('stance_id')

        stance = get_object_or_404(Stance, pk=stance_id)

        return render(request, self.template_name, {
            'stance': stance,
        })
