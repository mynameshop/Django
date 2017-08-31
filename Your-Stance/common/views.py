import json

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.edit import View
from profiles.models import Profile
from questions.models import Question


def search_ajax_view(request):
    q = request.GET.get('q')
    type = request.GET.get('type', 'questions')

    """
    Details __contains may pose performance issue in case some of questions containing
    very long detail list.
    """

    if type == 'questions':
        results = Question.objects.filter(Q(slug__icontains=q) | Q(details__icontains=q)).values('pk', 'slug')
    else:
        results = Profile.objects.filter(Q(user__username__icontains=q)).values('pk', 'user__username')

    return HttpResponse(json.dumps(list(results)))


def authenticated_user_member_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME,
                                       login_url=settings.LOGIN_URL):
    return user_passes_test(
        lambda u: u.is_active and hasattr(u, "profile"),
        login_url=settings.LOGIN_URL,
        redirect_field_name=redirect_field_name
    )(view_func)


class ProfileView(View):
    profile = None

    @method_decorator(authenticated_user_member_required)
    def dispatch(self, request, *args, **kwargs):
        self.profile = request.user.profile
        response = super(ProfileView, self).dispatch(request, *args, **kwargs)
        return response
