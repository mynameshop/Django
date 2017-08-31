from __future__ import unicode_literals
from django.db import models
from django.utils.functional import cached_property
from settings import AUTH_USER_MODEL
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField 
from pinax.stripe.models import Coupon, Subscription
from apps.canvas_gadget.models import ProjectRequest
import os
from apps.canvas_gadget.utils import get_absolute_url

from apps.base.models import ModelCreatetAtMixin
import settings

ANIMATION_CASCADE = 0
ANIMATION_INDIVIDUAL = 1
ANIMATION_TYPE_CHOICES = (
    (ANIMATION_CASCADE, 'cascade'),
    (ANIMATION_INDIVIDUAL, 'individual'),
)

LIGHT_MODEL_DEFAULT = [
    {
        'type': 'HemisphericLight',
        'position': {
            'x': 0,
            'y': 1,
            'z': 0,
        },
        'range': 1,
        'intensity': 1,
        'color': {
            'diffuse': { 'r': 1, 'g': 1, 'b': 1},
            'specular': { 'r': 1, 'g': 1, 'b': 1},
            'groundColor': { 'r': 1, 'g': 1, 'b': 1},
        }
    },
    {
        'type': 'DirectionalLight',
        'position': {
            'x': 0,
            'y': -5,
            'z': 0,
        },
        'direction': {
            'x': 0,
            'y': 1,
            'z': 0,
        },
        'range': 5,
        'intensity': 0.4,
        'diffuse': { 'r': 1, 'g': 1, 'b': 1},
        'specular': { 'r': 1, 'g': 1, 'b': 1},
        'groundColor': { 'r': 1, 'g': 1, 'b': 1},
    },
    {
        'type': 'HemisphericLight',
        'position': {
            'x': 0,
            'y': -1,
            'z': 0,
        },
        'range': 1,
        'intensity': 1,
        'diffuse': { 'r': 1, 'g': 1, 'b': 1},
        'specular': { 'r': 1, 'g': 1, 'b': 1},
        'groundColor': { 'r': 1, 'g': 1, 'b': 1},
    },
]

LIGHT_MODEL_USAGE = [
    {
        'type': 'HemisphericLight',
        'position': {
            'x': 0,
            'y': 1,
            'z': 0,
        },
        'range': 1,
        'intensity': 1,
        'color': {
            'diffuse': { 'r': 1, 'g': 1, 'b': 1},
            'specular': { 'r': 1, 'g': 1, 'b': 1},
            'groundColor': { 'r': 1, 'g': 1, 'b': 1},
        }
    },
    {
        'type': 'DirectionalLight',
        'position': {
            'x': 0,
            'y': -5,
            'z': 0,
        },
        'direction': {
            'x': 0,
            'y': 1,
            'z': 0,
        },
        'range': 5,
        'intensity': 0.4,
        'diffuse': { 'r': 1, 'g': 1, 'b': 1},
        'specular': { 'r': 1, 'g': 1, 'b': 1},
        'groundColor': { 'r': 1, 'g': 1, 'b': 1},
    },
    {
        'type': 'PointLight',
        'position': {
            'x': 0,
            'y': -5,
            'z': 0,
        },
        'range': 5,
        'intensity': 0.4,
        'diffuse': { 'r': 1, 'g': 1, 'b': 1},
        'specular': { 'r': 1, 'g': 1, 'b': 1},
        'groundColor': { 'r': 1, 'g': 1, 'b': 1},
    },
    {
        'type': 'SpotLight',
        'position': {
            'x': 0,
            'y': -5,
            'z': 0,
        },
        'direction': {
            'x': 0,
            'y': 1,
            'z': 0,
        },
        'angle': 0.8,
        'exponent': 2,
        'range': 5,
        'intensity': 0.4,
        'diffuse': { 'r': 1, 'g': 1, 'b': 1},
        'specular': { 'r': 1, 'g': 1, 'b': 1},
        'groundColor': { 'r': 1, 'g': 1, 'b': 1},
    },
]

def get_project_media_folder(project_id):
    return 'projects/{0}'.format(project_id)

def upload_to_projects_media(instance, filename):
    return '{0}/{1}'.format(get_project_media_folder(instance.id), filename)

def remove_media(name):
    path = os.path.join(settings.MEDIA_ROOT, name)
    if os.path.exists(path):
        os.remove(path)

def upload_project_thumbnail(instance, filename):
    name = upload_to_projects_media(instance, 'thumbnail.png')
    remove_media(name)
    return name

def upload_project_logo(instance, filename):
    name = upload_to_projects_media(instance, 'logo.png')
    remove_media(name)
    return name

def upload_model2d_to_media(instance, filename):
    return '{0}/model2d/{1}'.format(get_project_media_folder(instance.project_id), filename)

def upload_model3d_gallery_to_media(instance, filename):
    model3d = instance.model3d
    return '{0}/model3d/{1}/gallery/{2}'.format(get_project_media_folder(model3d.project_id), model3d.id, filename)

def upload_model_to_media(instance, filename):
    if filename.endswith('.babylon'):
        filename = filename + '.json'
    return '{0}/model3d/{1}/{2}'.format(get_project_media_folder(instance.project_id), instance.id, filename)

def upload_animation_to_media(instance, filename):
    return '{0}/model3d/{1}/{2}'.format(get_project_media_folder(
        instance.animation_model.model3d.project_id), 
        instance.animation_model.model3d_id, filename
    )

def upload_texture_to_media(instance, filename):
    settings.BASE_DIR
    name = '{0}/model3d/{1}/{2}'.format(
        get_project_media_folder(instance.model3d.project_id), 
        instance.model3d_id, 
        filename
    )
    fullname = os.path.join(settings.MEDIA_ROOT, name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return name


def upload_environment_to_media(instance, filename):
    return '{0}/environment/{1}'.format(get_project_media_folder(instance.project_id), filename)

def upload_skybox_file(instance, filename):
    name = 'skybox/{0}/{1}'.format(instance.id, filename)
    return name
def replace_skybox_file(instance, filename):
    name = upload_skybox_file(instance, filename)
    remove_media(name)
    return name
def upload_skybox_thumbnail(instance, filename):
    return replace_skybox_file(instance, 'thumbnail.jpg')
def upload_skybox_nx(instance, filename):
    return replace_skybox_file(instance, 'skybox_nx.jpg')
def upload_skybox_ny(instance, filename):
    return replace_skybox_file(instance, 'skybox_ny.jpg')
def upload_skybox_nz(instance, filename):
    return replace_skybox_file(instance, 'skybox_nz.jpg')
def upload_skybox_px(instance, filename):
    return replace_skybox_file(instance, 'skybox_px.jpg')
def upload_skybox_py(instance, filename):
    return replace_skybox_file(instance, 'skybox_py.jpg')
def upload_skybox_pz(instance, filename):
    return replace_skybox_file(instance, 'skybox_pz.jpg')

class WithUpload(models.Model):
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            images = {}
            for field in self._meta.get_fields():
                if field.get_internal_type() == 'FileField':
                    field_name = field.name
                    images[field_name] = getattr(self, field_name, None)
                    setattr(self, field_name, None)
            super().save(*args, **kwargs)
            for field_name in images:
                setattr(self, field_name, images[field_name])
        super().save(*args, **kwargs)

class Skybox(ModelCreatetAtMixin):
    name =  models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128)
    thumbnail = models.ImageField(upload_to = upload_skybox_thumbnail, null=True, blank=True)
    nx = models.ImageField(upload_to = upload_skybox_nx, null=True, blank=True)
    ny = models.ImageField(upload_to = upload_skybox_ny, null=True, blank=True)
    nz = models.ImageField(upload_to = upload_skybox_nz, null=True, blank=True)
    px = models.ImageField(upload_to = upload_skybox_px, null=True, blank=True)
    py = models.ImageField(upload_to = upload_skybox_py, null=True, blank=True)
    pz = models.ImageField(upload_to = upload_skybox_pz, null=True, blank=True)
    
    class Meta:
        verbose_name = _('skybox')
        verbose_name_plural = _('skyboxes')
        ordering = ['id',]
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            images = {}
            for field in self._meta.get_fields():
                if field.get_internal_type() == 'FileField':
                    field_name = field.name
                    images[field_name] = getattr(self, field_name, None)
                    setattr(self, field_name, None)
            super().save(*args, **kwargs)
            for field_name in images:
                setattr(self, field_name, images[field_name])
        super().save(*args, **kwargs)
    
    @property
    def media_url(self):
        return '{0}{1}'.format(settings.MEDIA_URL, upload_skybox_file(self, ''))
    
class Groundplane(ModelCreatetAtMixin):
    name =  models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to = 'groundplane')
    
    class Meta:
        verbose_name = _('groundplane')
        verbose_name_plural = _('groundplanes')
        ordering = ['id',]
        
    def __str__(self):
        return self.name
    
class Light(models.Model):
    name = models.CharField(max_length=32, unique=True)
    source = JSONField(default=LIGHT_MODEL_DEFAULT)
    
    def __str__(self):
        return self.name
    
class Environment(models.Model):
    skybox = models.ForeignKey(Skybox, default=1)
    show_background = models.BooleanField(default = False)
    gradient_top_hue = models.FloatField(default = 0.5)
    gradient_top_lightness = models.FloatField(default = 0.5)
    gradient_bottom_hue = models.FloatField(default = 0.5)
    gradient_bottom_lightness = models.FloatField(default = 0.5)
    gradient_offset = models.FloatField(default = 0)
    
    show_ground_plane = models.BooleanField(default = False)
    ground_plane = models.ForeignKey(Groundplane, default=1)
    ground_plane_scale = models.FloatField(default = 1.0)
    
    show_shadow = models.BooleanField(default = False)
    show_reflective = models.BooleanField(default = False)
    reflective_amount = models.FloatField(default = 0)
    
    camera_upper_beta_limit =  models.FloatField(default = 1.5)
    light = models.ForeignKey(Light, default=1)
    
    class Meta:
        abstract = True
        
class SlimScroll(models.Model):
    slim_scroll_color = models.CharField(max_length=7, default='#ffffff',help_text=_(u'HEX color, as #RRGGBB'))
    
    class Meta:
        abstract = True

class Project(ModelCreatetAtMixin, Environment, SlimScroll):
    owner = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, blank=True, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField(blank=True, null=True)
    description = models.CharField(max_length=512)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=upload_project_thumbnail)
    subscription = models.ForeignKey(Subscription, null=True, blank=True)
    logo_image = models.ImageField(null=True, blank=True, upload_to=upload_project_logo)
    logo_url = models.URLField(null=True, blank=True, default='')
    projectrequest = models.OneToOneField(ProjectRequest, blank=True, null=True)
    
    show_cg_label = models.BooleanField(default=True)
    
    popup_show = models.BooleanField(default=True)
    popup_text = models.CharField(max_length=32, blank=True, null=True, 
        help_text='"Click or swipe to interact with the product" by default'
    )
    popup_extra_style = models.CharField(max_length=256, blank=True, null=True,
        help_text='for example: <code>top: 50%; left: 50%; transform: translate(-50%, -50%);</code>'
    )
    
    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ['name',]
        
    def __str__(self):
        return self.name
    
    @cached_property
    def plan_amount_per_month(self):
        plan = self.get_or_create_plan()
        interval_count = plan.interval_count if plan.interval_count > 0 else 1
        discount_percent_off = 0.0
        if self.coupon_id:
            discount_percent_off = self.coupon.percent_off
        return float(plan.amount/interval_count) * (1 - discount_percent_off/100.0)
    
    def get_or_create_plan(self):
        '''
        возвращает план для текущего проекта. 
        создает новый план, если плана для проекта не существует.
        '''
        from apps.billing import utils as billing_utils
        plan = billing_utils.get_or_create_plan_by_project(self)
        return plan
    
    @cached_property
    def projectrequest_status(self):
        projectrequest = self.projectrequest
        if projectrequest:
            return projectrequest.status
        return 0
        
    @cached_property
    def subscription_is_active(self):
        s = self.subscription
        return s and s.status in ('active', 'trialing')
    
    @cached_property
    def subscription_status_display_text(self):
        result = 'This project has not been published.'
        s = self.subscription
        if s:
            if s.status in ('active', 'trialing'):
                if s.cancel_at_period_end == 1:
                    result = 'Payment cycle for this product will expire: {0}'.format(s.current_period_end)
                else:
                    result = 'Payment cycle for this product ends: {0}'.format(s.current_period_end)
            elif s.status in ('canceled'):
                result = 'Payment cycle for this product has been canceled.'
            elif s.status in ('unpaid', 'past_due'):
                result = 'This project has not been published.'
        return result
            
class CalloutStyle(ModelCreatetAtMixin):
    image = models.ImageField(upload_to='style/callout', null=False, blank=False)
    
    class Meta:
        verbose_name = _('callout style')
        verbose_name_plural = _('callout styles')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    @property
    def json_model(self):
        data = {
            'id': self.id,
            'image': get_absolute_url(self.image.url),
        }
        return data
    
class LineStyle(ModelCreatetAtMixin):
    image = models.ImageField(upload_to='style/line', null=False, blank=False)
    thumbnail = models.ImageField(upload_to='style/line', null=False, blank=False)
    
    class Meta:
        verbose_name = _('line style')
        verbose_name_plural = _('line styles')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    @property
    def json_model(self):
        data = {
            'id': self.id,
            'image': get_absolute_url(self.image.url),
            'thumbnail': get_absolute_url(self.thumbnail.url),
        }
        return data
    
class AnchorStyle(ModelCreatetAtMixin):
    image = models.ImageField(upload_to='style/anchor', null=False, blank=False)
    
    class Meta:
        verbose_name = _('anchor style')
        verbose_name_plural = _('anchor styles')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    @property
    def json_model(self):
        data = {
            'id': self.id,
            'image': get_absolute_url(self.image.url),
        }
        return data

class Model2D(ModelCreatetAtMixin):
    project = models.ForeignKey(Project)
    image = ThumbnailerImageField(
        upload_to=upload_model2d_to_media,
    )
    
class Model3D(ModelCreatetAtMixin):
    project = models.ForeignKey(Project)
    file = models.FileField(upload_to=upload_model_to_media)
    thumbnail = ThumbnailerImageField(
        resize_source=dict(size=(256, 256), sharpen=True),
        upload_to=upload_model_to_media, 
        blank=True, 
        null=True, 
        default='',
    )
    thumbnail_tmp = ThumbnailerImageField(
        resize_source=dict(size=(85, 85), sharpen=True),
        upload_to=upload_model_to_media, 
        blank=True, 
        null=True, 
        default='',
    )
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    camera_pos_x = models.FloatField(default = 0.0045000000000007334)
    camera_pos_y = models.FloatField(default = 0.7674)
    camera_pos_z = models.FloatField(default = -2.9879999999999995)
    rotate_camera = models.BooleanField(default=True)
    camera_min_distance = models.FloatField(default = 1.5)
    camera_max_distance = models.FloatField(default = 6)
    
    class Meta:
        verbose_name = _('3d model')
        verbose_name_plural = _('3d models')
        ordering = ['id',]
        
    def __str__(self):
        return self.file.name
    
    @property
    def media_url(self):
        return self.file.url
    
    @cached_property
    def urls_for_textures(self):
        urls = set()
        for t in self.texture_set.all():
            urls.add(get_absolute_url(t.file.url))
        return list(urls)
    
    def json_model(self, is_published=False):
        thumb = self.thumbnail if is_published else (self.thumbnail_tmp or self.thumbnail)
        materials = []
        for mat in self.modelmaterial_set.all():
            materials.append(mat.json_model)
            
        flares = []
        for flare in self.modellensflare_set.all():
            flares.append(flare.json_model)
            
        callouts = []
        for callout in self.callout_set.all():
            callouts.append(callout.json_model)
        
        try:
            animation_model = self.animationmodel
        except:
            animation_model = None
        
        model3dgallery_set = []
        for g in self.model3dgallery_set.all():
            try:
                model3dgallery_set.append(get_absolute_url(g.image['medium'].url))
            except:
                pass
            
        data = {
            'id': self.pk,
            'pk': self.pk,
            'model': get_absolute_url(self.file.url),
            'file': get_absolute_url(self.file.url),
            'thumbnail': {
                'small': {
                    'url': get_absolute_url(thumb['small'].url) if thumb else '',
                }
            },
            'textures': self.urls_for_textures,
            'materials': materials,
            'flares': flares,
            'callouts': callouts,
            'animation': animation_model.json_model(is_published) if animation_model else {},
            'camera_pos': {
                'x': self.camera_pos_x,
                'y': self.camera_pos_y,
                'z': self.camera_pos_z,
            },
            'camera_upper_beta_limit': self.camera_upper_beta_limit_value,
            'rotate_camera': self.rotate_camera,
            'camera_min_distance': self.camera_min_distance,
            'camera_max_distance': self.camera_max_distance,
            'default_material': {'id': 9, 'name': 'Matte Finish'},
            'model3dgallery': model3dgallery_set
        }
        
        data['animations'] = data['animation']
        return data
    
    @cached_property
    def camera_upper_beta_limit_value(self):
        return self.project.camera_upper_beta_limit
    
class Model3DGallery(ModelCreatetAtMixin):
    model3d = models.ForeignKey(Model3D)
    image = ThumbnailerImageField(
        upload_to=upload_model3d_gallery_to_media,
    )
    numv = models.IntegerField()
    numh = models.IntegerField()
    
    class Meta:
        verbose_name = _('3d model gallery')
        verbose_name_plural = _('3d model galleries')
        ordering = ['numv', 'numh']

class AnimationModel(ModelCreatetAtMixin):
    model3d = models.OneToOneField(Model3D)
    type = models.IntegerField(choices=ANIMATION_TYPE_CHOICES, default=ANIMATION_CASCADE)
    
    class Meta:
        verbose_name = _('animation model')
        verbose_name_plural = _('animation models')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    def json_model(self, is_published=False):
        data = {
            "type": self.get_type_display(),
            "animations": [],
        }
        for animation in self.animation_set.all().order_by('id'):
            data['animations'].append(animation.json_model(is_published=is_published))
        return data
    
class Animation(ModelCreatetAtMixin):
    animation_model = models.ForeignKey(AnimationModel)
    name = models.CharField(max_length=64)
    target = models.CharField(max_length=64)
    forward = JSONField(blank=True, null=True)
    reverse = JSONField(blank=True, null=True)
    auto_reverse = models.BooleanField(default=True)
    
    thumbnail = ThumbnailerImageField(
        resize_source=dict(size=(256, 256), sharpen=True),
        upload_to=upload_animation_to_media, 
        blank=True, 
        null=True, 
        default='',
    )
    thumbnail_tmp = ThumbnailerImageField(
        resize_source=dict(size=(85, 85), sharpen=True),
        upload_to=upload_animation_to_media, 
        blank=True, 
        null=True, 
        default='',
    )
    logo_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('animation')
        verbose_name_plural = _('animations')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    def json_model(self, is_published=False):
        thumb = self.thumbnail if is_published else (self.thumbnail_tmp or self.thumbnail)
        data = {
            "id": self.id,
            "name": self.name,
            "target": self.target,
            "forward": self.forward,
            "reverse": self.reverse,
            "auto_reverse": self.auto_reverse,
            "thumbnail": {
                "small": {
                    "url": get_absolute_url(thumb["small"].url) if thumb else '',
                }
            },
            "logo_url": self.logo_url or '',
        }
        return data
    
class Callout(ModelCreatetAtMixin):
    model3d = models.ForeignKey(Model3D)
    callout_style = models.ForeignKey(CalloutStyle)
    line_style = models.ForeignKey(LineStyle)
    anchor_style = models.ForeignKey(AnchorStyle)
    label = models.CharField(max_length = 40)
    text = models.CharField(max_length = 80)
    x = models.FloatField(default = 0.0)
    y = models.FloatField(default = 0.0)
    z = models.FloatField(default = 0.0)
    
    class Meta:
        verbose_name = _('callout')
        verbose_name_plural = _('callouts')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    @property
    def json_model(self):
        data = {
            'id': self.id,
            'model3d': self.model3d_id,
            'text': self.text,
            'label': self.label,
            'pos': {
                'x': self.x,
                'y': self.y,
                'z': self.z,
            },
            'anchor_style': self.anchor_style.json_model,
            'line_style': self.line_style.json_model,
            'callout_style': self.callout_style.json_model,
        }
        return data
        
class Texture(ModelCreatetAtMixin):
    model3d = models.ForeignKey(Model3D)
    file = models.FileField(upload_to=upload_texture_to_media)
    
    class Meta:
        verbose_name = _('texture')
        verbose_name_plural = _('textures')
        ordering = ['id',]
        
    def __str__(self):
        return self.file.name
   
class Material(ModelCreatetAtMixin):
    name =  models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128)
    thumbnail = models.ImageField(upload_to='material')
    data = JSONField(default={})
    normal_map = models.ImageField(upload_to='material', null=True, blank=True)
    
    class Meta:
        verbose_name = _('material')
        verbose_name_plural = _('materials')
        ordering = ['name',]
        
    def __str__(self):
        return self.name
    
    @property
    def json_model(self):
        data = {
            'id': self.id,
            'name': self.name,
            'thumbnail': get_absolute_url(self.thumbnail.url),
            'normal_map': get_absolute_url(self.normal_map.url) if self.normal_map else '',
        }
        data.update(self.data)
        return data
    
class LensFlare(ModelCreatetAtMixin):
    name =  models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128)
    thumbnail = models.ImageField(upload_to='lens_flare')
    band_1 = models.ImageField(upload_to='lens_flare')
    band_2 = models.ImageField(upload_to='lens_flare')
    main_flare = models.ImageField(upload_to='lens_flare')
    hexigon_shape = models.ImageField(upload_to='lens_flare')
    
    class Meta:
        verbose_name = _('lens flare')
        verbose_name_plural = _('lens flares')
        ordering = ['name',]
        
    def __str__(self):
        return self.name
    
    
    @property
    def json_model(self):
        data = {
            'id': self.id,
            'name': self.name,
            'thumbnail': get_absolute_url(self.thumbnail.url),
            'band_1': get_absolute_url(self.band_1.url),
            'band_2': get_absolute_url(self.band_2.url),
            'main_flare': get_absolute_url(self.main_flare.url),
            'hexigon_shape': get_absolute_url(self.hexigon_shape.url),
        }
        return data
    
class ModelMaterial(ModelCreatetAtMixin):
    model3d = models.ForeignKey(Model3D)
    material = models.ForeignKey(Material)
    compNum = models.IntegerField()
    subCompNum = models.IntegerField(default=-1)
    
    class Meta:
        verbose_name = _('model material')
        verbose_name_plural = _('model materials')
        ordering = ['id',]
        unique_together = (('model3d', 'compNum', 'subCompNum'),)
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    @property
    def json_model(self):
        data = self.material.json_model
        data['compNum'] = self.compNum
        data['subCompNum'] = self.subCompNum
        return data

class ModelLensFlare(ModelCreatetAtMixin):
    model3d = models.ForeignKey(Model3D)
    lensflare = models.ForeignKey(LensFlare)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    
    class Meta:
        verbose_name = _('model lens flare')
        verbose_name_plural = _('model lens flares')
        ordering = ['id',]
        
    def __str__(self):
        return '{0}'.format(self.id)
    
    @property
    def json_model(self):
        data = self.lensflare.json_model
        data['pos'] = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }
        return data