WEDGE_KEY = 'fb_wedge'
NEXT_KEY = 'fb_next'


def get_social_account(request):
    if not hasattr(request, 'user'):
        return None
    
    if request.user.is_authenticated():
        return request.user.socialaccount_set.all().first()


def is_wedge_eligible(request):
    social_account = get_social_account(request)
    
    if social_account is None:
        return False
    
    return social_account.extra_data.get(WEDGE_KEY, False) == True
        

def set_wedge_egilibility(request, flag, social_account=None):
    if social_account is None:
        social_account = get_social_account(request)
    
    if social_account is None:
        return
    
    social_account.extra_data[WEDGE_KEY] = flag
    social_account.save()
    
    