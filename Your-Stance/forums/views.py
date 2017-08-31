from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Forum, Thread, Comment
from .forms import NewThreadForm, ReplyThreadForm
from questions.models import Question

class ForumsView(View):
    template_name = 'forums/forums.html'

    def get(self, request, *args, **kwargs):
        forums = Forum.objects.all().order_by('priority')
        return render(request, self.template_name, {
            'forums': forums,
        })


class ForumView(View):
    template_name = 'forums/forum.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        forum = Forum.objects.get(slug=slug)
        threads = Thread.objects.filter(forum=forum.id)
        return render(request, self.template_name, {
            'forum': forum,
            'threads': threads
        })


class ThreadView(View):
    def get(self, request, *args, **kwargs):
        thread_id = self.kwargs['pk']
        thread = Thread.objects.get(pk=thread_id)
        comments = Comment.objects.filter(thread=thread)
        if thread.forum:
            forum = Forum.objects.get(pk=thread.forum.pk)
            template_name = 'forums/forum_thread.html'
            return render(request, template_name, {
                'comments': comments,
                'thread': thread,
                'reply_thread_form': ReplyThreadForm(),
                'forum': forum,
            })
        else:
            question = Question.objects.get(pk=thread.question.pk)
            template_name = 'forums/question_thread.html'
            return render(request, template_name, {
                'comments': comments,
                'thread': thread,
                'reply_thread_form': ReplyThreadForm(),
                'question': question,
            })


class NewForumThreadView(LoginRequiredMixin, View):
    template_name = 'forums/new_forum_thread.html'

    def get(self, request, *args, **kwargs):

        slug = self.kwargs['slug']
        forum = Forum.objects.get(slug=slug)
        new_thread_form = NewThreadForm()
        return render(request, self.template_name, {
            'new_thread_form': new_thread_form,
            'forum': forum
        })

    def post(self, request, *args, **kwargs):

        form = NewThreadForm(request.POST)
        if form.is_valid():
            slug = self.kwargs['slug']
            forum = Forum.objects.get(slug=slug)
            thread = Thread()
            thread.title = form.cleaned_data['title']
            thread.author = request.user
            thread.forum = forum
            thread.save()
            comment = Comment()
            comment.author = request.user
            comment.comment_text = form.cleaned_data['comment_text']
            comment.thread = thread
            comment.save()
            return HttpResponseRedirect(reverse('forums:thread', args=[thread.id]))


class NewQuestionThreadView(View):
    template_name = 'forums/new_question_thread.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        question = Question.objects.get(slug=slug)
        new_thread_form = NewThreadForm()
        return render(request, self.template_name, {
            'new_thread_form': new_thread_form,
            'question': question
        })

    def post(self, request, *args, **kwargs):
        form = NewThreadForm(request.POST)
        if form.is_valid():
            slug = self.kwargs['slug']
            question = Question.objects.get(slug=slug)
            thread = Thread()
            thread.title = form.cleaned_data['title']
            thread.author = request.user
            thread.question = question
            thread.save()
            comment = Comment()
            comment.author = request.user
            comment.comment_text = form.cleaned_data['comment_text']
            comment.thread = thread
            comment.save()
            return HttpResponseRedirect(reverse('forums:thread', args=[thread.id]))


class ReplyThreadView(View):

    def post(self, request, *args, **kwargs):
        form = ReplyThreadForm(request.POST)
        if form.is_valid():
            thread = Thread.objects.get(pk=self.kwargs['pk'])
            thread.num_comments = thread.num_comments + 1
            comment = Comment()
            comment.author = request.user
            comment.comment_text = form.cleaned_data['comment_text']
            comment.thread = thread
            comment.save()
            thread.last_comment = comment
            thread.save()
            return HttpResponseRedirect(reverse('forums:thread', args=[thread.id]))
