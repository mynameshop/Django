from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from notifications import models
from profiles import models as pmodels
from questions import models as qmodels
from django.contrib.sites.models import Site


def check_mail_enabled(type, profile):
    type_field = {
        models.NEW_QUESTION: 'notification_question',
        models.FOLLOWED: 'notification_follower',
        models.MENTION: 'notification_mention',
        models.FORUM_MENTION: 'notification_mention',
        models.REPLY_FORUM_COMMENT: 'notification_comment',
        models.REPLY_STANCE_COMMENT: 'notification_comment',
        models.LIKE: 'notification_like',
        models.AGREE: 'notification_agrees',
    }

    if type in type_field:
        field = type_field[type]
        value = getattr(profile, field)
        return value
    else:
        return False


def broadcast_notification(profiles, type, **kwargs):
    for p in profiles:
        send_notification(type, user_to=p.user, **kwargs)


def broadcast_question_notification(question):
    profiles = pmodels.Profile.objects.prefetch_related('user') \
        .filter(Q(is_proxy=False) & ~Q(user__email=None))
    broadcast_notification(profiles=profiles, type=models.NEW_QUESTION, question=question)


def send_notification(type, no_dbentry=False, **kwargs):
    notification = models.Notification(
        user_to=kwargs.get('user_to'),
        notification_type=type,
    )
    d = Context({"site": Site.objects.get_current()})
    email_template = None
    email_title = ''

    if type == models.NEW_QUESTION:
        question = kwargs['question']
        email_template = get_template('notifications/email/new_question.html')
        email_title = 'New question'
        d.update({"question": question})
    elif type == models.REPLY_STANCE_COMMENT:
        notification.user_from = kwargs.get('user_from')
        notification.stance = kwargs.get('stance')
        email_template = get_template('notifications/email/stance_comment.html')
        email_title = notification.user_from.username + ' left you a comment on Your Stance'
    elif type == models.REPLY_FORUM_COMMENT:
        notification.user_from = kwargs.get('user_from')
        notification.comment = kwargs.get('comment')
        email_template = get_template('notifications/email/forum_comment.html')
        email_title = notification.user_from.username + ' left you a comment on Your Stance'
    elif type == models.AGREE:
        notification.user_from = kwargs.get('user_from')
        notification.stance = kwargs.get('stance')
        email_template = get_template('notifications/email/agree.html')
        email_title = 'Someone selected one of your stances as their own'
    elif type == models.LIKE:
        star = kwargs.get('star')
        notification.user_from = star.user
        notification.stance = star.stance
        email_template = get_template('notifications/email/star.html')
        email_title = 'Someone starred one of your posts'
    elif type == models.MENTION or type == models.FORUM_MENTION:
        notification.user_from = kwargs.get('user_from')
        notification.stance = kwargs.get('stance')
        notification.comment = kwargs.get('comment')
        email_template = get_template('notifications/email/mention.html')
        email_title = 'You\'ve been mentioned!'
    elif type == models.FOLLOWED:
        notification.user_from = kwargs.get('user_from')
        email_template = get_template('notifications/email/follow.html')
        email_title = 'New Follower'

    if not no_dbentry:
        notification.save()

    if email_template and not notification.user_to.profile.is_proxy and \
            notification.user_to.email and \
            check_mail_enabled(type, notification.user_to.profile):
        print "Sending email to", notification.user_to.email
        d.update({'n': notification})

        html_content = email_template.render(d)
        from_email = 'Your Stance <notifications@yourstance.com>'

        if settings.NOTIFICATIONS_EMAIL_TARGET is not None:
            print "Using dev email", settings.NOTIFICATIONS_EMAIL_TARGET
            target_email = settings.NOTIFICATIONS_EMAIL_TARGET
        else:
            target_email = notification.user_to.email

        msg = EmailMultiAlternatives(email_title, None, from_email, [target_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=qmodels.Question)
def question_save_handler(sender, instance, created, **kwargs):
    if created:
        broadcast_question_notification(instance)
