from common.views import ProfileView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from forums.models import Thread
from questions.forms import SuggestQuestionForm
from questions.models import SuggestedQuestion
from stances.forms import NewStanceForm
from stances.models import Stance
from .models import Question, Answer


class QuestionsView(View):
    template_name = 'questions/questions.html'

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()

        Question.objects.mark_choices(questions, request.user)

        return render(request, self.template_name, {
            'questions': questions,
        })


class RankingsView(View):
    template_name = 'questions/rankings.html'

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        return render(request, self.template_name, {
            'questions': questions,
        })


class QuestionView(View):
    template_name = 'questions/question.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        question = get_object_or_404(Question, slug__iexact=slug)

        current_url = request.resolver_match.url_name
        if current_url == 'question_new':
            pro_stances = Stance.objects.filter(question=question.id, choice='p').order_by('-created')
            con_stances = Stance.objects.filter(question=question.id, choice='c').order_by('-created')
        elif current_url == 'question_top':
            pro_stances = Stance.objects.filter_counts_and_order(question=question.id, choice='p')
            con_stances = Stance.objects.filter_counts_and_order(question=question.id, choice='c')
        elif current_url == 'question_famous':
            pro_stances = Stance.objects.filter_counts_and_order(question=question.id, choice='p',
                                                                 user__profile__is_famous=True)
            con_stances = Stance.objects.filter_counts_and_order(question=question.id, choice='c',
                                                                 user__profile__is_famous=True)
        else:
            pro_stances = Stance.objects.filter_counts_and_order(question=question.id, choice='p')
            con_stances = Stance.objects.filter_counts_and_order(question=question.id, choice='c')

        top_10 = Stance.objects.top10(question)
        threads = Thread.objects.filter(question=question.id).order_by('-created')[:15]

        # TODO:  REMOVE THIS! Place it in smart spots
        question.update_votes()

        question.pro_winning = True
        if question.pro_percentage < 51:
            question.pro_winning = False

        my_stance = question.get_user_stance(request.user)
        new_stance_form = NewStanceForm(initial={'question': question.id})

        last_stance = None
        if "last_stance_id" in request.session:
            last_stance = Stance.objects.get(pk=request.session["last_stance_id"])
            del request.session["last_stance_id"]

        unanswered_questions = Question.objects.order_by('?')[:5]

        return render(request, self.template_name, {
            'question': question,
            'pro_stances': pro_stances,
            'con_stances': con_stances,
            'my_stance': my_stance,
            'current_url': current_url,
            'threads': threads,
            'new_stance_form': new_stance_form,
            'unanswered_questions': unanswered_questions,
            'top_10': top_10,
            'last_stance': last_stance
        })


class SuggestQuestionView(View):
    template_name = 'questions/suggest.html'

    def post(self, request, *args, **kwargs):
        suggestion = SuggestedQuestion()

        if request.user.is_authenticated():
            suggestion.user = request.user

        form = SuggestQuestionForm(request.POST, instance=suggestion)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Thank you for your input. Your question is awaiting admin approval.')
            return redirect(reverse('questions:suggest_question'))

        return render(request, self.template_name, {
            'form': form,
        })

    def get(self, request, *args, **kwargs):
        form = SuggestQuestionForm()

        return render(request, self.template_name, {
            'form': form,
        })


class GauntletView(TemplateView, ProfileView):
    template_name = 'questions/gauntlet.html'
    question = None

    def get(self, request, *args, **kwargs):
        self.question = self.profile.unanswered_questions.first()
        if not self.question:
            if request.user.profile.follow_process_is_complete:
                return redirect(reverse('home'))
            else:
                return redirect(reverse('profiles:follow_friends'))
        return super(GauntletView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        pro_stances = Stance.objects.filter_counts_and_order(question=self.question.id, choice='p')[:20]
        con_stances = Stance.objects.filter_counts_and_order(question=self.question.id, choice='c')[:20]
        new_stance_form = NewStanceForm(initial={'question': self.question.id})
        last_stance = None

        if "last_stance_id" in self.request.session:
            last_stance = Stance.objects.get(pk=self.request.session["last_stance_id"])
            del self.request.session["last_stance_id"]

        total_questions = self.profile.question_list_count
        answered_questions = self.profile.user.profile.answered_questions_count
        data = {
            'question': self.question,
            'pro_stances': pro_stances,
            'con_stances': con_stances,
            'new_stance_form': new_stance_form,
            'last_stance': last_stance,
            'hide_gauntlet_warning': True,
            'total_questions': total_questions,
            'answered_questions': answered_questions,
        }
        kwargs.update(data)
        return super(GauntletView, self).get_context_data(**kwargs)


def next_question(request):
    question = request.user.profile.unanswered_questions_plus_skipped.first()
    return HttpResponseRedirect(reverse('questions:question', args=[question.slug]))


def check_new_stance(choice, stance_text):
    errors = []
    if not choice:
        errors.append("Select your stance")
    if not stance_text:
        errors.append("Please enter your stance text")
    return errors


def make_new_stance_ajax(request):
    result = {}

    question_id = request.POST.get('question_id')
    stance_text = request.POST.get('stance_text')
    choice = request.POST.get('choice[]')

    errors = check_new_stance(choice, stance_text)

    if len(errors) == 0:
        question = Question.objects.get(pk=question_id)
        answer = Answer(user=request.user)
        stance = Stance(question=question, user=request.user, stance_text=stance_text, choice=choice)
        stance.save()
        answer.stance = stance
        answer.save()
        result['ok'] = True
        result['stance_text'] = stance.stance_text
        result['choice'] = stance.choice

    else:
        result['ok'] = False
        result['errors'] = errors

    return JsonResponse(result)


def select_stance_ajax(request):
    result = {}

    stance_id = request.GET.get('stance_id')

    stance = Stance.objects.get(pk=stance_id)
    answer = stance.question.get_user_answer(request.user)

    if not answer:
        answer = Answer()
        answer.user = request.user

    answer.stance = stance
    answer.save()

    result['ok'] = True
    result['stance_text'] = stance.stance_text
    result['choice'] = stance.choice

    return JsonResponse(result)
