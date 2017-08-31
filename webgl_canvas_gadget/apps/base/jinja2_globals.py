from apps.base.decorators import jinja2_global
from datetime import datetime
from django.utils.dateformat import format

@jinja2_global
def now(format_string='%d.%m.%y %H:%M:%S'):
    return datetime.now().strftime(format_string)

@jinja2_global
def date(dt, format_string):
    return format(dt, format_string)

@jinja2_global
def thumbnail(source, **kwargs):
    from easy_thumbnails.templatetags import thumbnail as _thumbnail
    try:
        thumbnail =  _thumbnail.get_thumbnailer(source).get_thumbnail(kwargs)
        return thumbnail.url
    except:
        return ''

@jinja2_global
def json_stringify(data):
    import json
    return json.dumps(data)

@jinja2_global
def is_debug():
    from settings import DEBUG
    return DEBUG