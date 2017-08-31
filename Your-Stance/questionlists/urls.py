from django.conf.urls import url

from . import views

app_name = 'questionlists'

urlpatterns = [
    url(r'^$', views.QuestionListsView.as_view(), name='questionlists'),
    url(r'^(?P<slug>[\w-]+)$',
        views.QuestionListView.as_view(), name='questionlist')
]
