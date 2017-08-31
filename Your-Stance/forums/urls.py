from django.conf.urls import url

from . import views

app_name = 'forums'
urlpatterns = [
    url(r'^forums/$', views.ForumsView.as_view(), name='forums'),

    url(r'^f/(?P<slug>[\w-]+)$', views.ForumView.as_view(), name='forum'),
    url(r'^thread/(?P<pk>[0-9]+)$', views.ThreadView.as_view(),
        name='thread'),
    url(r'^new/forum/thread/(?P<slug>[-\w]+)$', views.NewForumThreadView.as_view(),
        name='new_forum_thread'),
    url(r'^new/question/thread/(?P<slug>[-\w]+)$', views.NewQuestionThreadView.as_view(),
        name='new_question_thread'),
    url(r'^thread/reply/(?P<pk>\d+)$',
        views.ReplyThreadView.as_view(), name='reply_thread'),
]
