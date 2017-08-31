from __future__ import unicode_literals
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db import transaction
from django.core import serializers
from settings import PINAX_STRIPE_PUBLIC_KEY
import json

from pinax.stripe.models import Card, Subscription

from .decorators import active_subscription_or_sample_required
from .models import (Project, Model3D, Model3DGallery, Texture, Skybox, Material, 
    LensFlare, CalloutStyle, LineStyle, AnchorStyle, Groundplane, ModelMaterial, 
    ModelLensFlare, Callout, Animation, AnimationModel, ANIMATION_TYPE_CHOICES
    )
from . import utils
from apps.billing.forms import CreditcardForm

class ProjectListView(ListView):
    model = Project
    allow_empty = False
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect(reverse("canvas_gadget:pricingpage"))

    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_add_card'] = CreditcardForm()
        context['STRIPE_PUBLIC_KEY'] = PINAX_STRIPE_PUBLIC_KEY
        return context
    

def get_model2d_model(qs):
    model = []
    for o in qs:
        model.append({
            'image': o.image.url,
            'thumbnail': {
                'small': {
                    'url': o.image['small'].url,
                }
            }
        })
    return model
    
def get_model3d_model(queriset, is_published=False):
    queriset = queriset.exclude(is_deleted=True)
    if is_published:
        queriset = queriset.filter(is_published=is_published)
    queriset = queriset.order_by('id')
    models = []
    for model in queriset:
        models.append(model.json_model(is_published=is_published))
    return models

class ProjectNewDetailView(DetailView):
    model = Project
    template_name = 'projects/project_new_detail.html'
    is_published = True
    
    @xframe_options_exempt
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(active_subscription_or_sample_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        project = self.get_object()
        context = super().get_context_data(**kwargs)
        context['HIDE_LOGO'] = self.request.GET.get('HIDE_LOGO', 'false').lower() == 'true'
        context['HIDE_THUMBNAILS'] = self.request.GET.get('HIDE_THUMBNAILS', 'false').lower() == 'true'
        context['MODELS3D'] = project.model3d_set.filter(is_deleted=False)
        context['MODELS2D'] = project.model2d_set.all()
        context['MATERIALS'] = Material.objects.all()
        
        materials_model = []
        for mat in context['MATERIALS']:
            materials_model.append(mat.json_model)
        context['MATERIALS_MODEL'] = materials_model
        
        project_model = serializers.serialize('json', [project], 
            fields=(
                'show_background',
                'gradient_top_hue',
                'gradient_top_lightness',
                'gradient_bottom_hue',
                'gradient_bottom_lightness',
                'gradient_offset',
                'show_ground_plane',
                'ground_plane_scale',
                'show_shadow',
                'show_reflective',
                'reflective_amount',
            )
        )
        skybox = project.skybox
        project_model = json.loads(project_model)
        project_model[0]['fields']['light'] = project.light.source
        project_model[0]['fields']['skybox'] = {
            'id': skybox.id,
            'url': skybox.media_url,
        }
        ground_plane = project.ground_plane
        if ground_plane:
            project_model[0]['fields']['ground_plane'] = {
                'id': ground_plane.id,
                'url': ground_plane.image.url,
            }
        context['PROJECT_MODEL'] = project_model
        context['PROJECT_MODEL'][0]['fields']['is_editor'] = False
        context['MODELS3D_MODEL'] = get_model3d_model(context['MODELS3D'], self.is_published)
        context['MODELS2D_MODEL'] = get_model2d_model(context['MODELS2D'])
        return context
    

class ProjectNewDetailCompactView(ProjectNewDetailView):
    model = Project
    template_name = 'projects/project_new_detail_compact.html'
    is_published = True
    
    @xframe_options_exempt
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['IS_COMPACT'] = True
        return context
    

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    is_published = True
    
    @xframe_options_exempt
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(active_subscription_or_sample_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        project = self.get_object()
        context = super().get_context_data(**kwargs)
        context['HIDE_UI'] = False
        context['MODELS3D'] = project.model3d_set.filter(is_deleted=False)
        context['MATERIALS'] = Material.objects.all()
        materials_model = []
        for mat in context['MATERIALS']:
            materials_model.append(mat.json_model)
        context['MATERIALS_MODEL'] = materials_model
        
        project_model = serializers.serialize('json', [project], 
            fields=(
                'show_background',
                'gradient_top_hue',
                'gradient_top_lightness',
                'gradient_bottom_hue',
                'gradient_bottom_lightness',
                'gradient_offset',
                'show_ground_plane',
                'ground_plane_scale',
                'show_shadow',
                'show_reflective',
                'reflective_amount',
            )
        )
        skybox = project.skybox
        project_model = json.loads(project_model)
        project_model[0]['fields']['light'] = project.light.source
        project_model[0]['fields']['skybox'] = {
            'id': skybox.id,
            'url': skybox.media_url,
        }
        ground_plane = project.ground_plane
        if ground_plane:
            project_model[0]['fields']['ground_plane'] = {
                'id': ground_plane.id,
                'url': ground_plane.image.url,
            }
        context['PROJECT_MODEL'] = project_model
        context['PROJECT_MODEL'][0]['fields']['is_editor'] = False
        context['MODELS3D_MODEL'] = get_model3d_model(project.model3d_set.filter(is_deleted=False), self.is_published)
        return context
    
class ProjectDetailCompactView(ProjectDetailView):
    model = Project
    template_name = 'projects/project_detail_compact.html'
    is_published = True
    
    @xframe_options_exempt
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class ProjectDetailBaseView(ProjectDetailView):
    model = Project
    
    @xframe_options_exempt
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['HIDE_UI'] = True
        return context
    
class ProjectEditView(ProjectDetailView):
    template_name = 'projects/project_update.html'
    is_published = False
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        project = self.get_object()
        context = super().get_context_data(**kwargs)
        context['SKYBOXES'] = Skybox.objects.all()
        context['GROUNDPLANE'] = Groundplane.objects.all()
        context['LENS_FRAMES'] = LensFlare.objects.all()
        
        context['CALLOUT_STYLE'] = CalloutStyle.objects.all()
        context['LINE_STYLE'] = LineStyle.objects.all()
        context['ANCHOR_STYLE'] = AnchorStyle.objects.all()
        
        project_model = serializers.serialize('json', [project], 
            fields=(
                'show_background',
                'gradient_top_hue',
                'gradient_top_lightness',
                'gradient_bottom_hue',
                'gradient_bottom_lightness',
                'gradient_offset',
                'show_ground_plane',
                'ground_plane_scale',
                'show_shadow',
                'show_reflective',
                'reflective_amount',
            )
        )
        skybox = project.skybox
        project_model = json.loads(project_model)
        project_model[0]['fields']['light'] = project.light.source
        project_model[0]['fields']['skybox'] = {
            'id': skybox.id,
            'url': skybox.media_url,
        }
        ground_plane = project.ground_plane
        if ground_plane:
            project_model[0]['fields']['ground_plane'] = {
                'id': ground_plane.id,
                'url': ground_plane.image.url,
            }
        context['PROJECT_MODEL'] = project_model
        context['PROJECT_MODEL'][0]['fields']['is_editor'] = True
        context['MODELS3D_MODEL'] = get_model3d_model(project.model3d_set.filter(is_deleted=False))
        return context
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = []
        from django.core.files.base import ContentFile
        import os

        if request.is_ajax():
            project = self.get_object()
            fields = ['environment_image', 'show_background', 'gradient_top_hue',
                      'gradient_top_lightness', 'gradient_bottom_hue',
                      'gradient_bottom_lightness', 'gradient_offset', 'show_ground_plane', 
                      'ground_plane', 'ground_plane_scale', 'show_shadow',
                      'show_reflective', 'reflective_amount', 'skybox',
                      ]
            for name in fields:
                val = request.POST.get(name, None)
                if val != None:
                    if project._meta.get_field(name).get_internal_type() == 'BooleanField':
                        val = (val == 'true')
                    elif project._meta.get_field(name).get_internal_type() == 'ForeignKey':
                        name = name + '_id'
                    setattr(project, name, val)
            project.save()
            
            project.model3d_set.filter(is_deleted=True).delete()
            model3d_index = {}
            for model3d in project.model3d_set.all():
                model3d.is_published = True
                if model3d.thumbnail_tmp:
                    if not model3d.thumbnail_tmp:
                            continue
                    model3d.thumbnail.save(os.path.basename(model3d.thumbnail_tmp.name), ContentFile(model3d.thumbnail_tmp.read()))
                    model3d.thumbnail_tmp.delete()
                model3d.save()
                try:
                    animation_model = model3d.animationmodel
                except:
                    animation_model = None
                if animation_model:
                    for animation in animation_model.animation_set.all():
                        if not animation.thumbnail_tmp:
                            continue
                        animation.thumbnail.save(os.path.basename(animation.thumbnail_tmp.name), ContentFile(animation.thumbnail_tmp.read()))
                        animation.thumbnail_tmp.delete()
                model3d_index[model3d.id] = model3d
                
            for data_model3d in json.loads(request.POST.get('models', [])):
                model3d = model3d_index.get(data_model3d['id'], None)
                if not model3d:
                    continue
                model3d.camera_pos_x = data_model3d['camera_pos']['x']
                model3d.camera_pos_y = data_model3d['camera_pos']['y']
                model3d.camera_pos_z = data_model3d['camera_pos']['z']
                model3d.save()
                
                for matetial_data in data_model3d['materials']:
                    try:
                        m = ModelMaterial.objects.get(
                            model3d = model3d, 
                            compNum = matetial_data['compNum'],
                            subCompNum = matetial_data.get('subCompNum', -1),
                        )
                    except ModelMaterial.DoesNotExist:
                        m = ModelMaterial(
                            model3d = model3d, 
                            compNum = matetial_data['compNum'],
                            subCompNum = matetial_data.get('subCompNum', -1),
                        )
                    m.material_id = matetial_data['id']
                    m.save()
                
                ModelLensFlare.objects.filter(model3d = model3d).delete()
                for flare_data in data_model3d['flares']:
                    f = ModelLensFlare(
                        model3d = model3d,
                        lensflare_id = flare_data['id'],
                        x = flare_data['pos']['x'],
                        y = flare_data['pos']['y'],
                        z = flare_data['pos']['z'],
                    )
                    f.save()
                for callout_data in data_model3d.get('callouts', []):
                    if not isinstance( callout_data['id'], int ):
                        callout_data['id'] = None
                        callout = Callout(
                            model3d = model3d,
                            x = callout_data['pos']['x'],
                            y = callout_data['pos']['y'],
                            z = callout_data['pos']['z'],
                            label = callout_data['label'],
                            text = callout_data['text'],
                            callout_style_id = callout_data['callout_style']['id'],
                            line_style_id = callout_data['line_style']['id'],
                            anchor_style_id = callout_data['anchor_style']['id'],
                        )
                        callout.save()
            
        return HttpResponse(json.dumps(data), content_type="application/json")
    
class Model3dCreateView(CreateView):
    model = Model3D
    
    @method_decorator(login_required)
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_project(self):
        return Project.objects.get(pk=self.request.POST['project_id'])
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = []
        if request.is_ajax():
            if request.FILES:
                obj = self.get_project()
                files = request.FILES.getlist('files[]')
                model3d_file = utils.get_accepted_3d_file(files)
                textures = utils.get_images(files)
                animation_model_json = utils.get_animation_model(files)
                model3d = Model3D(
                    project = obj,
                )
                model3d.save()
                model3d.file = model3d_file
                model3d.save()
                
                for t_file in textures:
                    texture = Texture(
                        model3d = model3d,
                    )
                    texture.save()
                    texture.file = t_file
                    texture.save()
                
                if animation_model_json:
                    utils.save_animation_json(model3d, animation_model_json)
                
                data = get_model3d_model(obj.model3d_set.all())
        return HttpResponse(json.dumps(data), content_type="application/json")
    
class Model3dEditView(DetailView):
    model = Model3D
    
    def get(self, request, *args, **kwargs):
        data = {}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        is_delete = (request.POST.get('is_deleted', None) == 'true')
        if is_delete:
            obj.is_deleted = True
            obj.save()
        elif request.FILES.get('thumbnail_tmp', None): 
            thumbnail_tmp = request.FILES.get('thumbnail_tmp')
            obj.thumbnail_tmp = thumbnail_tmp
            obj.save()
        data = get_model3d_model(obj.project.model3d_set.all())
        return HttpResponse(json.dumps(data), content_type="application/json")
    
class Model3DGalleryView(DetailView):
    model = Model3D
    template_name = 'projects/model_3dgallery.html'
    
    def decode_base64_file(self, data):

        def get_file_extension(file_name, decoded_file):
            import imghdr
    
            extension = imghdr.what(file_name, decoded_file)
            extension = "jpg" if extension == "jpeg" else extension
    
            return extension
    
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
    
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
    
            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                TypeError('invalid_image')
    
            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = get_file_extension(file_name, decoded_file)
    
            complete_file_name = "%s.%s" % (file_name, file_extension, )
    
            return ContentFile(decoded_file, name=complete_file_name)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        clear = request.POST.get('clear', False)
        if not clear:
            image = json.loads(request.POST.get('image'))
            Model3DGallery.objects.create(
                model3d = obj,
                numv = image['numv'],
                numh = image['numh'],
                image = self.decode_base64_file(image['data']),
            )
        else:
            obj.model3dgallery_set.all().delete()
        data = {}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
class AnimationEditView(DetailView):
    model = Animation
    
    def get(self, request, *args, **kwargs):
        data = {}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.FILES.get('thumbnail_tmp', None): 
            thumbnail_tmp = request.FILES.get('thumbnail_tmp')
            obj.thumbnail_tmp = thumbnail_tmp
            obj.save()
        data = get_model3d_model(obj.animation_model.model3d.project.model3d_set.all())
        return HttpResponse(json.dumps(data), content_type="application/json")
    