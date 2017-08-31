import json
import requests
import twitter
import pickle
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from allauth.socialaccount import models as smodels
from profiles.models import Follow


class Friend(object):
    
    def __init__(self, avatar, name, uid, data={}):
        self._meta = None
        self.avatar = avatar
        self.name = name
        self.data = data
        self.uid = uid
        self.invitable = False
        self.followed = False
        self.type = ''
        self.user = None
    
    def __str__(self):
        return self.name
    
    def jsonize(self):
        self.data = json.dumps(self.data)
    
 


class FriendGetter(object):
    def __init__(self, user):
        self.user = user
        self.paging_data = {}
        self.next = None
        
    def lookup(self, friends):
        pass
    
    def get_friends(self):
        return []
    
    def get_name(self):
        return None
    
    def is_connected(self):
        return True
    
    def set_paging_data(self, data):
        self.paging_data = data
    
    def jsonize_data(self, friends):
        for f in friends:
            f.data = json.dumps(f.data)
    
    def get_next(self):
        return self.next
    

class DummyFriendGetter(FriendGetter):
    def get_friends(self):    
        return [
        ]
        
    def get_name(self):
        return 'not implemented service'
    

class FBFriendGetter(FriendGetter):
    
    def __init__(self, user):
        super(FBFriendGetter, self).__init__(user)
        self.social_user  = self.user.socialaccount_set.filter(provider='facebook').first()
        
    
    @staticmethod
    def find_socialaccount(friend):

        social_account_candidates = smodels.SocialAccount.objects.filter(extra_data__contains=friend.name) #.first()

        for sa in social_account_candidates:
            if sa.extra_data['name'] == friend.name:
                return sa

        return None
        

    def lookup(self, all_friends, invitable_friends):
        #all_uids = [f.name for f in all_friends ]
        invitable_uids = [f.name for f in invitable_friends ]
        for f in all_friends:
            f.type = 'fb'
            f.data = {}
            if f.name in invitable_uids:
                i = invitable_uids.index(f.name)
                f.invitable = True
                f.invitable_uid = invitable_friends[i].uid
            
            social_account = FBFriendGetter.find_socialaccount(f)
                
            if social_account:
                f.user = social_account.user
                f.followed = False
                if Follow.objects.filter(follower=self.user.profile, followed=f.user.profile).first():
                    f.followed = True                    
                    

    def parse_friend_response(self, response):
        friends = []
        for friend in response['data']:
            friend_object = Friend(friend['picture']['data']['url'], friend['name'], friend['id'])
            friend_object.invitable_uid = None
            friends.append(friend_object)
        return friends
    
    def get_friends(self):
        
        social_user  = self.social_user
        token = social_user.socialtoken_set.all().first().token
        
        if social_user:
            
            url = u'https://graph.facebook.com/v2.1/me/' \
                  u'invitable_friends/?fields=about,id,name,picture,link' \
                  u'&access_token={}&uid={}&limit=1000'.format(
            
                     token,
                     social_user.uid,
                      
                  )
            
            response_invitable = requests.get(url).json()
            
            max_res = self.paging_data['max_res']
            next = self.paging_data['next']
            
            
            if next:
                url = next
            else:
                url = u'https://graph.facebook.com/v2.1/{}/' \
                  u'taggable_friends?fields=about,id,name,picture,link' \
                  u'&access_token={}&uid={}&limit={}'.format(
                     social_user.uid,
                     token,
                     social_user.uid,
                     max_res,
                  )
            
            response = requests.get(url).json()
            try:
                self.next = response['paging']['next']
            except KeyError:
                self.next = None
            
            
            friends = self.parse_friend_response(response)
            invitable_friends = self.parse_friend_response(response_invitable)
            self.lookup(friends, invitable_friends)  
            self.get_friend_fbids(friends, token)
            self.jsonize_data(friends)
            return friends #temporary, use friends and set invitable id
        else:
            return []
    
    
    def get_friend_fbids(self, friends, token):
        url ='https://graph.facebook.com/v2.0/me?fields=friends&access_token={}'.format(token)
        response = requests.get(url).json()
        
        if 'friends' in response and 'data' in response['friends']:
            f_names = [f['name'] for f in response['friends']['data'] ]
         
            for f in friends:
                try:
                    i = f_names.index(f.name)
                except ValueError:
                    continue
                f.data['fbid'] = response['friends']['data'][i]['id']
                f.data['token'] = token
     

    def get_name(self):
        return 'facebook'
    
    def is_connected(self):
        return self.social_user is not None

    
class GoogleFriendGetter(FriendGetter):
    def __init__(self, user):
        super(GoogleFriendGetter, self).__init__(user)
        self.next = None
        self.social_user  = self.user.socialaccount_set.filter(provider='google').first()
        if self.social_user:
            token_object = smodels.SocialToken.objects.get(account=self.social_user)
            self.access_token = token_object.token
        else:
            self.access_token = None
        
    def lookup_friend(self, friend_object, friend_entry):
        #invitable_uids = [f.name for f in invitable_friends ]
        emails =  [f['address'] for f in friend_entry['gd$email']]
        if self.user.email in emails:
            return False
        user = User.objects.filter(email__in=emails).first()
        
        if not user:
            friend_object.invitable = True
        else:
            friend_object.user = user
            friend_object.followed = False
            if Follow.objects.filter(follower=self.user.profile, followed=friend_object.user.profile).first():
                friend_object.followed = True  
        
        return True
    
    def fetch_avatar(self, friend_entry):
        links = friend_entry['link']
        for link in links:
            if link['type'] == 'image/*' and link['rel'] == 'http://schemas.google.com/contacts/2008/rel#photo':
                return link['href']+'?access_token='+self.access_token
        
    
    def get_next_url(self, response_data):
        links = response_data['feed']['link']
        for link in links:
            if link['rel']=='next':
                return link['href']
    
    def get_friends(self):    
        
        friends = []
        max_res = self.paging_data['max_res']
        next = self.paging_data['next']
        
        if not next:
            url = 'https://www.google.com/m8/feeds/contacts/default/full' \
                + '?access_token=' \
                + self.access_token + '&max-results='+max_res+'&alt=json'
        else:
            url = next+'&access_token='+self.access_token
        
        
        response = requests.get(url)
        
        #print response.text
        
        response_data = response.json()
        
        if max_res is not None:
            self.next = self.get_next_url(response_data)
            
            
            
        entries = response_data['feed']['entry']
        
        for e in entries:
            name = ''
            if e['title']['$t']: 
                name = e['title']['$t']
 
            try:
                email = e['gd$email'][0]['address']
            except KeyError:
                continue
                
            if name:
                friend_name = name + ' ('+email+')'
            else:
                friend_name = email
            
            
            friend_object = Friend(self.fetch_avatar(e), friend_name, None)
            friend_object.data['email'] = email
            #friend_object.data['google_avatar'] = self.fetch_avatar(e)
            
            if self.lookup_friend(friend_object, e):
                friend_object.jsonize()
                friends.append(friend_object)
            

        return friends
    
    def get_next(self):
        return self.next
    
    def get_name(self):
        return 'google'
    
    def is_connected(self):
        return self.social_user is not None
    
    
class TwitterFriendGetter(FriendGetter):
    SESSION_LIST_KEY = 'twitter_contacts'
    SESSION_FETCHTIME_KEY = 'twitter_fetch_timestamp'
    SESSION_LIFETIME = 900 #in seconds so its 15 minutes
    def __init__(self, user, request):
        super(TwitterFriendGetter, self).__init__(user)
        self.request = request
        self.social_user  = self.user.socialaccount_set.filter(provider='twitter').first()
        if self.social_user:
            self.social_token = smodels.SocialToken.objects.get(account=self.social_user)
        
    def is_connected(self):
        return self.social_user is not None
    
    def session_store(self, friends):
        timestamp = time.time()
        serialized_friends = pickle.dumps(friends)
        self.request.session[TwitterFriendGetter.SESSION_LIST_KEY] =  serialized_friends
        self.request.session[TwitterFriendGetter.SESSION_FETCHTIME_KEY] = timestamp
    
    def session_restore(self):
        
        serialized_friends = self.request.session.get(TwitterFriendGetter.SESSION_LIST_KEY, None)
        if serialized_friends is None:
            return None
        friends = pickle.loads(serialized_friends)
        return friends
    
    def get_session_age(self):
        timestamp = self.request.session.get(TwitterFriendGetter.SESSION_FETCHTIME_KEY, None)
        if timestamp is None:
            return TwitterFriendGetter.SESSION_LIFETIME
        else:
            return time.time() - timestamp
        
    
    def get_api(self):
        social_app = self.social_user.get_provider().get_app(self.request)
        
        api = twitter.Api(consumer_key=social_app.client_id,
                      consumer_secret=social_app.secret,
                      access_token_key=self.social_token.token,
                      access_token_secret=self.social_token.token_secret)
        return api
    
    def fetch_friends(self):
        print "-------------Fetch friends"
        api = self.get_api()
        status = api.GetRateLimitStatus('friends')
        
        
        if status['resources']['friends']['/friends/list']['remaining']==0:
            return []
        else:
            twitter_friends = api.GetFriends()
    
        friends = []
        
        for friend in twitter_friends:
            friend_object = Friend(friend.GetProfileImageUrl(), friend.name, friend.GetId())
            friends.append(friend_object)
            
        return friends
    
    def lookup_friends(self, friends):
        #accounts = smodels.SocialAccount.objects.filter(provider='twitter')
       
        for friend in friends:
            
            candidate_account = smodels.SocialAccount.objects.filter(
                    Q(provider='twitter') 
                    & Q(uid=friend.uid)).first()
            
            if candidate_account:
                friend.user = candidate_account.user
                friend.followed = False
                if Follow.objects.filter(follower=self.user.profile, followed=friend.user.profile).first():
                    friend.followed = True  
            else:
                friend.invitable = True
                friend.invitable_uid = friend.uid
                
    
    def get_friends(self):    
        session_age = self.get_session_age()
        
        friends = self.session_restore()
        
        if friends is None or session_age >= TwitterFriendGetter.SESSION_LIFETIME:
            friends = self.fetch_friends()
            self.session_store(friends)
        else:
            print "from session"
            
        max_res = int(self.paging_data['max_res'])
        next = self.paging_data['next']
        
        if next is None:
            next = 0
        else:
            next = int(next)
        
        from_i = int(self.request.GET.get('from_i', 0))
        
        self.next = max_res + next
        self.lookup_friends(friends)
        return friends[next:max_res+next]

    def get_next(self):
        return self.next
    
    def get_name(self):
        return 'twitter'
    



def send_invitation_email(user, email):
    
    if settings.NOTIFICATIONS_EMAIL_TARGET is not None:
            print "Using dev email", settings.NOTIFICATIONS_EMAIL_TARGET
            email = settings.NOTIFICATIONS_EMAIL_TARGET
    
    context = Context({
           'user': user,
    })
    
    email_template = get_template('profiles/invitation_email.html')
    email_title = 'Yourstance invitation'    
    html_content = email_template.render(context)
    from_email = 'Your Stance <notifications@yourstance.com>'
    msg = EmailMultiAlternatives(email_title, None, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    return email