from django.contrib.auth.models import User
from django.test import TestCase
from profiles.models import Profile
from questions import answers_helper as ah
from questions.models import Question, Answer
from stances.models import Stance


class AgreeMarkTest(TestCase):
    def setUp(self):
        q1 = Question(slug='test1')
        q1.save()
        q2 = Question(slug='test2')
        q2.save()
        q3 = Question(slug="test3")
        q3.save()
        u1 = User(username="u1")
        u1.save()
        u2 = User(username="u2")
        u2.save()
        p1 = Profile(user=u1)
        p2 = Profile(user=u2)
        p1.save()
        p2.save()
        q1s1u1 = Stance(question=q1, choice='p', user=u1, stance_text="")
        q1s1u1.save()
        q1s2u1 = Stance(question=q1, choice='c', user=u1, stance_text="")
        q1s2u1.save()
        q1s2u2 = Stance(question=q1, choice='p', user=u2, stance_text="")
        q1s2u2.save()
        q2s1u1 = Stance(question=q2, choice='p', user=u1, stance_text="")
        q2s1u1.save()
        q2s1u2 = Stance(question=q2, choice='c', user=u2, stance_text="")
        q2s1u2.save()

        q3s1u1 = Stance(question=q3, choice='p', user=u1, stance_text="")
        q3s1u1.save()

        q1au1 = Answer(stance=q1s1u1, user=u1)
        q1au1.save()
        q1au2 = Answer(stance=q1s2u2, user=u2)
        q1au2.save()
        q2au1 = Answer(stance=q2s1u1, user=u1)
        q2au1.save()
        q2au2 = Answer(stance=q2s1u2, user=u2)
        q2au2.save()

        q3au1 = Answer(stance=q3s1u1, user=u1)
        q3au1.save()

        self.u1 = u1
        self.u2 = u2

    def test_agree_answer(self):
        u1_answers = Answer.objects.filter(user=self.u1)
        u2_answers = Answer.objects.filter(user=self.u2)

        ah.mark_agree_answer(u1_answers, self.u2)
        self.assertEqual(len(u1_answers), 3)
        self.assertEqual(len(u2_answers), 2)
        self.assertEqual(u1_answers[0].agree, 'a')
        self.assertEqual(u1_answers[1].agree, 'd')
        self.assertEqual(u1_answers[2].agree, None)

        ah.mark_agree_answer(u2_answers, self.u1)
        self.assertEqual(u2_answers[0].agree, 'a')
        self.assertEqual(u2_answers[1].agree, 'd')
