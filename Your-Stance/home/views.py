from django.contrib.auth.models import User
from django.views.generic import TemplateView
from forums.models import Thread
from questions.models import Question
from home import feed


class HomeView(TemplateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["home/feed/feed.html"]
        return ['home/home.html']

    def get_context_data(self, **kwargs):
        if self.request.is_ajax():
            from_i = int(self.request.GET.get('from', 0))
            feed_data = feed.compile_feed(from_i, feed.FEED_LIMIT)
            context = {'feed_data': feed_data}
        else:
            feed_data = feed.compile_feed(0, feed.FEED_LIMIT)
            users = User.objects.prefetch_related('profile').order_by('-date_joined')[:20]
            questions = Question.objects.order_by('-created')[:10]
            threads = Thread.objects.order_by('-modified')[:8]
            context = {
                'questions': questions,
                'feed_data': feed_data,
                'threads': threads,
                'users': users,
                'per_page': feed.FEED_LIMIT,
            }
        kwargs.update(context)
        return super(HomeView, self).get_context_data(**kwargs)
