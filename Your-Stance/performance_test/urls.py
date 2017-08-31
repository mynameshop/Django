from django.conf.urls import url
from . import views
from common.regular_expressions import username

app_name = 'performance_test'
urlpatterns = [
    url(r'^stance_list$', views.stancelist_test),
    url(r'^question_list$', views.questionlist_test),
    url(r'^user_list$', views.userlist_test),
    url(r'^thread_list$', views.threadlist_test),
    url(r'^answers/(?P<username>{0})/$'.format(username), views.answerlist_test),
    url(r'^follow/(?P<username>{0})/$'.format(username), views.follow_test),
    url(r'^counters/(?P<username>{0})/$'.format(username), views.counters_test),
    url(r'^base$', views.middleware_test),
]