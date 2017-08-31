from django import template
register = template.Library()

@register.filter
def pretty_choice(value):
    if (value=='p'):
        return "for"
    elif (value=='c'):
        return "against"
    else:
        return "usnure"
