from django.contrib.auth import logout


class ProxyUserCheckMiddleware(object):
    def process_request(self, request):
        pass
        user = request.user
        if not user.is_anonymous():

            try:
                profile = user.profile
            except AttributeError:
                return

            if profile.is_proxy:
                logout(request)
