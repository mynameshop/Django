import sys
from django.conf import settings
from django.utils import translation
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

class DjangoTranslator(object):
    def ugettext(self, *args):
        return translation.ugettext(*args)

    def ungettext(self, *args):
        return translation.ungettext(*args)

def get_app_modules():
    for app_label in settings.INSTALLED_APPS:
        mod_name = '.'.join((app_label, 'jinja2_globals'))
        try:
            __import__(mod_name, {}, {}, [], 0)
            yield sys.modules[mod_name]
        except ImportError:
            pass

def install_globals(env):
    for mod in get_app_modules():
        for name in dir(mod):
            global_ = getattr(mod, name)
            if getattr(global_, 'jinja2_global', False):
                env.globals[name] = global_
            elif getattr(global_, 'jinja2_filter', False):
                env.filters[name] = global_
            elif getattr(global_, 'jinja2_test', False):
                env.tests[name] = global_

def environment(**options):
    env = Environment(**options)
    install_globals(env)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.install_gettext_translations(DjangoTranslator())
    return env