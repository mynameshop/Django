from django.conf.urls import url
from common.regular_expressions import username
from . import views

app_name = 'stances'
urlpatterns = [
    url(r'^stance/edit/(?P<stance_id>[0-9]+)$', views.EditStanceView.as_view(), name='stance_edit'),
    url(r'^stance/select$', views.select_stance, name='select'),
    url(r'^stance/skip$', views.skip_stance, name='skip_stance'),
    url(r'^stance/new$', views.NewStanceView.as_view(), name='new_stance'),
    url(r'^stance/reply/(?P<stance_id>[0-9]+)$', views.ReplyStanceView.as_view(), name='reply'),
    url(r'^stance/star/(?P<stance_id>[0-9]+)$', views.star_stance, name='star'),
    url(r'^stance/remove/(?P<stance_id>[0-9]+)$', views.remove_stance, name='remove'),
    url(r'^stance/citation/(?P<stance_id>[0-9]+)$', views.CitationView.as_view(), name='citation'),
    url(r'^s/stance_modal$', views.modal_content, name="stance_modal_ajax"),
    url(r'^s/stances_content$', views.stances_content, name="stance_content_ajax"),
    url(r'^(?P<username>{0})/(?P<question_slug>[-\w]+)$'.format(username),
        views.StanceView.as_view(), name='stance'),
    url(r'^(?P<username>{0})/(?P<question_slug>[-\w]+)/(?P<stance_id>[0-9]+)$'.format(username),
        views.StanceView.as_view(), name='stance'),

]
