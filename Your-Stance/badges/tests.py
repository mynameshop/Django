from django.test import TestCase

from django.contrib.auth.models import User
from badges.models import Badge, ProfileBadge
from questions.models import Answer,Question
from stances.models import Stance
from badges.helper import *

def make_test_profile(name='testDude'):
    u = User(username=name)
    u.save()
    p = Profile(name=name, user=u)
    p.save()
    return p

def make_basic_seed():
    Badge(type=Badge.TYPE_PIONEER, title='Test poineer').save()
    Badge(type=Badge.TYPE_GURU, title='Test guru').save()
    Badge(type=Badge.TYPE_BRAVE, title='Test brave').save()
    Badge(type=Badge.TYPE_TEST, title='Test test').save()
    Badge.PIONEER_THRESHOLD = 4


class HelperTest(TestCase):
    def setUp(self):
        make_basic_seed()
        self.bulb = make_test_profile('Misha')        
        self.nolly = make_test_profile('Nolly')
    
    def test_pioneer(self):
        self.assertEqual(Badge.PIONEER_THRESHOLD , 4)
        self.assertEqual(user_has_badge(self.bulb, Badge.TYPE_PIONEER), True)
        self.assertEqual(user_has_badge(self.nolly, Badge.TYPE_PIONEER), True)
        mark = make_test_profile('Mark')
        sponce = make_test_profile('Spencer')
        jake = make_test_profile('Jake')
        self.assertEqual(user_has_badge(mark, Badge.TYPE_PIONEER), True)
        self.assertEqual(user_has_badge(sponce, Badge.TYPE_PIONEER), True)
        self.assertEqual(user_has_badge(jake, Badge.TYPE_PIONEER), False)
        
    
    def test_guru(self):
        Badge.GURU_THRESHOLD = 4
        u_jc = make_test_profile('JCDenton')
        u_pd = make_test_profile('PaulDenton')
        u_pm = make_test_profile('PhilipMead')
        u_an = make_test_profile('AnnaNavarre')
        
        self.assertEqual(user_has_badge(u_jc, Badge.TYPE_GURU), False)
        
        q = Question(slug='test')
        q.save()
        s = Stance(question=q, choice='p', stance_text='Bravery is not a function of firepower', user=u_jc.user)
        s.save()
        
        Answer(user=u_pd.user, stance=s).save()
        Answer(user=u_pm.user, stance=s).save()
        Answer(user=u_an.user, stance=s).save()
        Answer(user=self.bulb.user, stance=s).save()
        
        self.assertEqual(user_has_badge(u_jc, Badge.TYPE_GURU), True)
        
    
    def test_basic(self):
        self.assertEqual(user_has_badge(self.bulb, Badge.TYPE_BRAVE), False)
        give_badge(self.bulb, Badge.TYPE_TEST)
        give_badge(self.bulb, Badge.TYPE_TEST)
        self.assertEqual(user_has_badge(self.bulb, Badge.TYPE_TEST), True)
        self.assertEqual(user_has_badge(self.bulb, Badge.TYPE_BRAVE), False)
        revoke_badge(self.nolly, Badge.TYPE_GURU)
        revoke_badge(self.nolly, Badge.TYPE_TEST)
        self.assertEqual(user_has_badge(self.nolly, Badge.TYPE_GURU), False)
        
    
class SyncTest(TestCase):
    def setUp(self):
        make_basic_seed()
        
        
    def test_sync(self):
        Badge.PIONEER_THRESHOLD = -1
        bulb = make_test_profile('Misha')        
        nolly = make_test_profile('Nolly')
        Badge.PIONEER_THRESHOLD = 10
        
        sync_badges(bulb)
        
        bulb_badges = get_profile_badges(bulb)
        
        self.assertEqual(len(bulb_badges), 2)
        self.assertEqual(bulb_badges[0].badge.type, Badge.TYPE_PIONEER)
        self.assertEqual(bulb_badges[1].badge.type, Badge.TYPE_TEST)
        
        nolly_badges = get_profile_badges(nolly)
        
        self.assertEqual(len(nolly_badges), 0)
        
        
    
        
        