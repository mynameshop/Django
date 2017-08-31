from django import template


register = template.Library()

def get_item(dictionary, key, subkey=None):
    if subkey is None:
        return dictionary.get(key)
    else:
        return dictionary.get(key).get(subkey)

def get_answer(item):
    if item is not None:
        return item['stance__choice']
    else:
        return None




register.filter('get_item', get_item)
register.filter('get_answer', get_answer)