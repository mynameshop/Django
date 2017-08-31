from django.conf.urls import url

from . import views

app_name = 'onboarding'
urlpatterns = [
    url(r'^edit_profile$', views.EditProfileView.as_view(), name='edit_profile'),
    url(r'^top_questions$', views.TopQuestionsView.as_view(), name='top_questions'),

]
