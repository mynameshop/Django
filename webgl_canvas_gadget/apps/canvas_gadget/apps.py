from __future__ import unicode_literals
from django.apps import AppConfig

class CanvasGadgetConfig(AppConfig):
    name = 'apps.canvas_gadget'
    
    def ready(self):
        from . import handlers