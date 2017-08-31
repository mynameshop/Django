from __future__ import unicode_literals
from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    name = 'apps.projects'
    
    def ready(self):
        from . import handlers