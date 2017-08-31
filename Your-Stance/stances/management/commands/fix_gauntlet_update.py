from django.core.management.base import BaseCommand
from profiles.models import Profile
from questions.models import Answer


class Command(BaseCommand):
    help = 'Remove duplicate answers'

    def handle(self, *args, **options):
        for_delete = []
        duplicates = dict()
        for answer in Answer.objects.all():
            if answer.user.pk not in duplicates:
                duplicates[answer.user.pk] = {}
            if answer.question.pk not in duplicates[answer.user.pk]:
                duplicates[answer.user.pk][answer.question.pk] = True
                continue
            for_delete.append(answer.pk)
        Answer.objects.filter(pk__in=for_delete).delete()
        Profile.objects.update(follow_process_is_complete=True)
