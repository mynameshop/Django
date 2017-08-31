from django import template


register = template.Library()

@register.assignment_tag
def mark_starred(*args, **kwargs):
    stance_pk = kwargs.get('stance_pk')
    stars = kwargs.get('stars')
    starred_text = kwargs.get('starred_text')
    unstarred_text = kwargs.get('unstarred_text')
    
    if stance_pk in stars:
        return starred_text
    else:
        return unstarred_text
