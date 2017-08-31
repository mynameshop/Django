from django.conf.urls import url

from . import views

app_name = 'notif'
urlpatterns = [
    url(r'^$', views.notifications, name='notifications'),
]
