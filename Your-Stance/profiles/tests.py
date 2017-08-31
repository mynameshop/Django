# -*- coding: utf-8 -*-

from django.test import TestCase
from profiles.slug import make_slug_username, get_next_number
from profiles.mentions import get_mentioned_users, parse_mention_text, mentions_to_hrefs
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User



class ProfileUsernameTest(TestCase):
    pass
#    def test_username_generation(self):
#        test_username = 'Tyler Waitt'
#        user = User()
#        user.username = test_username
#        user.save()
#        self.assertEqual(user.username, 'TylerWaitt')
#        user = User()
#        user.username = test_username
#        user.save()
#        self.assertEqual(user.username, 'TylerWaitt1')
#        user = User()
#        user.username = test_username
#        user.save()
#        self.assertEqual(user.username, 'TylerWaitt2')
#        n = get_next_number('TylerWaitt', user)
#        self.assertEqual(n, 2)
    
#    def test_case_insensitive_generation(self):
#        user = User()
#        user.username = 'Trent Reznor'
#        user.save()
#        self.assertEqual(user.username, 'TrentReznor')
#        user = User()
#        user.username = 'TRENT ReznoR'
#        user.save()
#        self.assertEqual(user.username, 'TRENTReznoR1')
        
        
class TestMentionObject(object):
    def __init__(self, fieldA=None):
        self.fieldA = fieldA
        
        
class MentionParseTest(TestCase):
    def setUp(self):
        self.usernames = [
            "AbrahamLincoln",
            "BillClinton",
            "GeorgeBush",
            "LechWalesa",
            "AngelaMerkel",
            "AdolfHitler",
            "TonyAbott"
        ]
        
        self.users_dict = {}
        
        for username in self.usernames:
            self.users_dict[username] = User(username=username)
            self.users_dict[username].save()
            
    
    def test_parse_mention(self):
        parses = parse_mention_text("When @GeorgeBush ivaded Iraq @BillClinton was retired. Those are assholes, @RandomDrunkGuy said.")
        self.assertItemsEqual(parses, ['GeorgeBush', 'BillClinton', 'RandomDrunkGuy', ]) 
        parses = parse_mention_text("@GeorgeBush said that his fater @GeorgeBush, heard about @BillClinton scandal.", unique=True)
        self.assertItemsEqual(parses, ['GeorgeBush', 'BillClinton'])
         
    def test_get_mentioned(self):
        users = get_mentioned_users("Most of Americans just love their @AbrahamLincoln president.")
        self.assertItemsEqual(users, [ self.users_dict['AbrahamLincoln'], ])
        users = get_mentioned_users("Our new president @AndrzejDuda is overdependent on his mentor @LechKaczynski.")
        self.assertItemsEqual(users, [])
        users = get_mentioned_users("Obvious info: @BillClinton is predesessor of @GeorgeBush.")
        self.assertItemsEqual(users, [
             self.users_dict['BillClinton'],
             self.users_dict['GeorgeBush'],
        ])
        
    def test_href_making(self):
        hrefed_mentions = mentions_to_hrefs("Obvious info: @BillClinton is predesessor of @GeorgeBush.")
        hrefed = 'Obvious info: <a href="/BillClinton">@BillClinton</a> is predesessor of <a href="/GeorgeBush">@GeorgeBush</a>.'
        self.assertEqual(hrefed_mentions, hrefed)

            