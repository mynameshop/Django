from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from .models import QuestionList, QuestionListItem
from questions.models import Question


class QuestionListsView(View):
    template_name = 'questionlists/questionlists.html'

    def get(self, request, *args, **kwargs):
        lists = QuestionList.objects.all()
        return render(request, self.template_name, {
            'lists': lists,
        })


class QuestionListView(View):
    template_name = 'questionlists/questionlist.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        qlist = QuestionList.objects.get(slug=slug)
        items = QuestionListItem.objects.filter(list=qlist)
        return render(request, self.template_name, {
            'qlist': qlist,
            'items': items
        })
