from __future__ import unicode_literals
from tastypie.api import Api
from tastypie.resources import Resource

api_v1 = Api(api_name='v1')

def register_resources(version='v1'):
    import sys, importlib, inspect
    
    p = 'apps.api.resources_{0}'.format(version)
    importlib.import_module(p)
    module = sys.modules[p]
    
    for key in dir(module):
        cls = getattr(module, key)
        if inspect.isclass(cls) and issubclass( cls, Resource ):
            print(key)
            api_v1.register( cls() )
            
register_resources(version='v1')