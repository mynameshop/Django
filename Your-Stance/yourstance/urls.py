import os
from common import views as base_views
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.contrib.auth import views
from home.views import HomeView
from profiles import views as profile_views

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    

    url(r'^password_reset/$', views.password_reset, {'template_name': 'pages/reset/reset.html', 'from_email':'notifications@yourstance.com'}, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, {'template_name': 'pages/reset/done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, {'template_name': 'pages/reset/confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, {'template_name': 'pages/reset/confirm_done.html'}, name='password_reset_complete'),

    url(r'^notifications/', include('notifications.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', include('loginas.urls')),
    url(r'^red/accounts/', include('allauth.urls')),
    url(r'^hello/', include('onboarding.urls')),
    url(r'^settings/', include('user_settings.urls')),
    url(r'^mentions', profile_views.mentions_ajax, name='mentions_ajax'),
    url(r'^users_ajax', profile_views.users_ajax, name='users_ajax'),
    url(r'^lists/', include('questionlists.urls')),
    url(r'^search_ajax/', base_views.search_ajax_view, name="search_ajax" ),
    url(r'^', include('forums.urls')),
    url(r'^', include('questions.urls')),
    url(r'^', include('pages.urls')),
    url(r'^', include('stances.urls')),
    url(r'^', include('profiles.urls')),
]

if 'performance_test' in settings.INSTALLED_APPS:
    urlpatterns = [url(r'^performance/', include('performance_test.urls'))] + urlpatterns


if settings.DEBUG404:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')} ),
    )

