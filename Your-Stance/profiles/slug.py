# -*- coding: utf-8 -*-

import unicodedata

from django.contrib.auth.models import User
from django.db.models import Q
from profiles.models import Profile

def strip_accents(text):
    """
    Unused due to allauth limitations
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)



def get_next_number(username, exclude_user=None):
    q = Q(username__icontains=username)
    
    if exclude_user is not None:
        q &= ~Q(pk=exclude_user.pk)
    
    user_duplicates = User.objects.filter(q)
    return len(user_duplicates)


def make_slug_username(username, exclude_user=None):
        #username = strip_accents(username)
        username = username.replace(' ', '')
        
        n = get_next_number(username, exclude_user)
        
        if n!=0:
            username = username+unicode(n)
        
        return username