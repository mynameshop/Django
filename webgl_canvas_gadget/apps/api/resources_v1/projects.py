from __future__ import unicode_literals
from tastypie import resources
from apps.projects.models import Project, Environment, Material
from apps.canvas_gadget.utils import get_absolute_url

class ProjectResource(resources.ModelResource):
    environment = resources.fields.DictField()
    model3d_set = resources.fields.ListField()
    material_set = resources.fields.ListField()
    
    class Meta:
        queryset = Project.objects.all()
        collection_name = 'project'
        resource_name = 'project'
        include_resource_uri = False
        list_allowed_methods = []
        detail_allowed_methods = ['get',]
        fields = ('id', 'name', 'description', 'thumbnail')
    
    def dehydrate_thumbnail(self, bundle):
        result = bundle.obj.thumbnail.url if bundle.obj.thumbnail else ''
        if result:
            result = get_absolute_url(result)
        return result
        
        
    def dehydrate_environment(self, bundle):
        result = {}
        
        for f in Environment._meta.get_fields():
            val = getattr(bundle.obj, f.name)
            if f.name == 'skybox':
                val = {
                    'id': val.id,
                    'url': get_absolute_url(val.media_url),
                }
            elif f.name == 'ground_plane':
                val = {
                    'id': val.id,
                    'url': get_absolute_url(val.image.url),
                }
            elif f.name == 'light':
                val = getattr(val, 'source')
            result[f.name] = val
        return result
    
    def dehydrate_model3d_set(self, bundle):
        result = []
        for obj in bundle.obj.model3d_set.filter(is_published=True, is_deleted=False):
            result.append(obj.json_model(is_published=True))
        return result
    
    def dehydrate_material_set(self, bundle):
        result = []
        materials = Material.objects.filter(modelmaterial__model3d__project = bundle.obj).distinct()
        for obj in materials:
            result.append(obj.json_model)
        return result
