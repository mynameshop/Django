from django.core.urlresolvers import reverse


def append_next(login_url, next_url, next_get_params=None):
    url = login_url+'?next='+next_url
    
    if next_get_params:
        sep = "?"
        for k, v in next_get_params.iteritems():
            url+=sep+str(k)+"="+str(v)
            sep = "&"
    
    return url
    
