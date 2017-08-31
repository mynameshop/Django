from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse
from profiles import wedge_helper as wh


# https://github.com/pennersr/django-allauth/issues/418#issuecomment-38391830

class Adapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):

        follow_redir = request.COOKIES.get('follow_friends_redir', None)

        url = super(Adapter, self).get_login_redirect_url(request)

        use_wedge = wh.is_wedge_eligible(request)

        if request.user.profile.should_gauntlet:
            request.session[wh.NEXT_KEY] = reverse('questions:gauntlet')

        referer = request.META.get('HTTP_REFERER', None)
        if use_wedge:
            request.session[wh.NEXT_KEY] = url
            return reverse('profiles:wedge')
        elif follow_redir != None and follow_redir != 'None':
            request.COOKIES['follow_friends_redir'] = None
            return follow_redir
        elif referer is not None and reverse('profiles:follow_friends') in referer:
            return referer
        else:
            url = request.session.pop(wh.NEXT_KEY, url)
            return url
