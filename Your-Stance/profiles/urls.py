from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from common.regular_expressions import username

from . import views

app_name = 'profiles'
urlpatterns = [
    url(r'^fb_wedge/$', views.FacebookWedgeView.as_view(), name='wedge'),
    url(r'^follow_friends/$', views.FollowFriendsView.as_view(), name='follow_friends'),
    url(r'^follow_friends/invite/$', views.friendlist_invite_email_ajax, name='follow_friends_invite'),
    url(r'^follow_friends/invite_twitter/$', views.friendlist_invite_twitter_ajax, name='follow_friends_invite_twitter'),
    url(r'^follow_friends/list/$', views.friendlist_ajax, name='follow_friends_list'),
    url(r'^follow_friends/google_connect/$', views.friendlist_google_connect, name='follow_friends_google_connect'),
    url(r'^follow_friends/twitter_connect/$', views.friendlist_twitter_connect, name='follow_friends_twitter_connect'),
    url(r'^p/$', views.ProfilesView.as_view(), name='profiles'),
    url(r'^comparsion/$', views.comparsion_ajax, name='comparsion'),
    url(r'^(?P<username>{0})/followers/$'.format(username), views.FollowersView.as_view(), name='followers'),
    url(r'^(?P<username>{0})/following/$'.format(username), views.FollowedView.as_view(), name='followed'),
    url(r'^(?P<username>{0})/follow/$'.format(username), views.follow_ajax, name='follow'),
    url(r'^(?P<username>{0})/$'.format(username), views.ProfileView.as_view(), name='profile'),
]
