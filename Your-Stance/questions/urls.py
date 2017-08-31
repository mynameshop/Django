from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^ajax/setstance/$', views.select_stance_ajax, name='ajax_set_stance'),
    url(r'^ajax/makestance/$', views.make_new_stance_ajax, name='ajax_make_stance'),
    url(r'^q/$', views.QuestionsView.as_view(), name='questions'),
    url(r'^rankings/$', views.RankingsView.as_view(), name='rankings'),
    url(r'^gauntlet/$', views.GauntletView.as_view(), name='gauntlet'),
    url(r'^q/suggest$', views.SuggestQuestionView.as_view(), name='suggest_question'),
    url(r'^q/next$', views.next_question, name='next'),
    url(r'^q/(?P<slug>[\w-]+)$', views.QuestionView.as_view(), name='question'),
    url(r'^q/(?P<slug>[\w-]+)/top$', views.QuestionView.as_view(), name='question_top'),
    url(r'^q/(?P<slug>[\w-]+)/new$', views.QuestionView.as_view(), name='question_new'),
    url(r'^q/(?P<slug>[\w-]+)/famous$', views.QuestionView.as_view(), name='question_famous'),
]
