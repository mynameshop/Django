from django.test import TestCase

from django.contrib.auth.models import User
from profiles.models import Profile

from stances.models import Stance
from questions.models import Question, Answer
from stances import orphan_collector as oc


class OrphanCollectorTest(TestCase):
    def setUp(self):
        self.u1 = User(username="u1")
        self.u1.save()
        self.u2 = User(username="u2")
        self.u2.save()
        self.p1 = Profile(user=self.u1)
        self.p2 = Profile(user=self.u2)
        self.p1.save()
        self.p2.save()
        self.collector = oc.OrphanCollector()
    
    
    def make_teststances_data(self):
        self.q1 = Question(slug="q1", details="")
        self.q2 = Question(slug="q2", details="")
        self.q1.save()
        self.q2.save()
        self.s1 = Stance(user=self.u1, question=self.q1, stance_text='a')
        self.s2 = Stance(user=self.u1, question=self.q2, stance_text='b')
        self.s1.save()
        self.s2.save()
        self.a1u1 = Answer(user=self.u1, stance=self.s2)
        self.a1u2 = Answer(user=self.u2, stance=self.s2)
        self.a2u2 = Answer(user=self.u2, stance=self.s1)
        self.a1u1.save()
        self.a1u2.save()
        self.a2u2.save()
        
    
    def test_queryset(self):
        self.make_teststances_data()
        orphans = self.collector.find_orphans()
        
        self.assertEqual(len(orphans), 1)
        self.assertEqual(orphans[0], self.s1)
        
    def test_assignment(self):
        self.make_teststances_data()
        self.collector.find_orphans(oc.OrphanCollector.assign_answer)
        orphans = self.collector.find_orphans()
        self.assertEqual(len(orphans), 0)
        answers = Answer.objects.filter(stance=self.s1, user=self.s1.user)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].created, self.s1.created)
        
        