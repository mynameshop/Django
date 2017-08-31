from __future__ import unicode_literals

from django.apps import AppConfig

class BadgesConfig(AppConfig):
    name = 'badges'
    
    def ready(self):
        from badges import events
