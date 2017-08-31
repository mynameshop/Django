from django.conf.urls import url

from . import views

app_name = 'settings'
urlpatterns = [
    #url(r'^register/$', views.RegisterView.as_view(), name='profiles'),
    url(r'^profile$', views.ProfileView.as_view(), name='profile'),
    url(r'^account$', views.AccountView.as_view(), name='account'),
    url(r'^notifications$', views.NotificationsView.as_view(), name='notifications'),
    url(r'^badges$', views.SettingsBadgesView.as_view(), name='badges'),
    url(r'^organizations$', views.SettingsOrganizationsView.as_view(), name='organizations'),
    url(r'^verification$', views.VerificationView.as_view(), name='verification'),
    url(r'^upload_avatar', views.upload_avatar, name='upload_avatar'),
]
