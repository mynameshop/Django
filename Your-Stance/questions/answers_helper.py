from django.conf import settings
from .models import Answer


def compare_stance_answers(stanceA, stanceB):
    if stanceA and stanceB and \
                    stanceA.choice != settings.UNSURE and stanceB.choice != settings.UNSURE:
        if stanceA.choice == stanceB.choice:
            return 'a'
        else:
            return 'd'


def mark_agree_answer(answers, user):
    for answer in answers:
        u_answer = Answer.objects.prefetch_related('user', 'stance', 'stance__question').filter(user=user,
                                                                                                stance__question=answer.stance.question).last()
        if u_answer:
            answer.agree = compare_stance_answers(u_answer.stance, answer.stance)
        else:
            answer.agree = None
