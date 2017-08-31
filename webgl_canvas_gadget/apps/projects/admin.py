from __future__ import unicode_literals
from django.contrib import admin
from django.urls import reverse
from .models import (Project, Model3D, Texture, Skybox, Material, LensFlare,
    CalloutStyle, LineStyle, AnchorStyle, Callout, Groundplane, ModelLensFlare,
    ModelMaterial, Animation, AnimationModel, Model2D, Light, Model3DGallery
)
from tabbed_admin import TabbedModelAdmin

import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe

class Model3DTabularInline(admin.TabularInline):
    model = Model3D
    exclude = ['thumbnail_tmp', 'is_deleted', 'is_published',
               'file', 'camera_pos_x', 'camera_pos_y', 'camera_pos_z']
    readonly_fields = ['model3d_admin_link']
    extra = 0
    
    def model3d_admin_link(self, obj):
        if obj.id:
            return '<a href="{0}" style="color: blue;" target="_blank">Edit 3d model</a>'.format(
                reverse('admin:projects_model3d_change', args=(obj.id,))
            )
        return '<span style="color: red;">3d model does not exist</span>'
    model3d_admin_link.allow_tags = True
    model3d_admin_link.short_description = '3d model'
    
class Model2DTabularInline(admin.TabularInline):
    model = Model2D
    fields = ['image']
    extra = 0

class ProjectAdmin(TabbedModelAdmin):
    readonly_fields = ['subscription_admin_link']
    list_display = ['name', 'owner', 'subscription_status_display']
    search_fields = ['owner__username', 'name']
    tab_overview = (
        (None, {
            'fields': [
                'name', 'slug', 'description', 'coupon', 'thumbnail', 'logo_image', 'logo_url', 
                'projectrequest', 'subscription_admin_link',
            ]
        }),
    )
    tab_env = (
        (None, {
            'fields': [
                'skybox', 'light', 'show_background', 
                'gradient_top_hue', 'gradient_top_lightness', 
                'gradient_bottom_hue', 'gradient_bottom_lightness', 
                'gradient_offset', 'show_ground_plane', 'ground_plane', 'ground_plane_scale', 
                'show_shadow', 'show_reflective', 'reflective_amount', 
                'slim_scroll_color', 'camera_upper_beta_limit',
            ]
        }),
    )
    tab_extra_ui = (
        (None, {
            'fields': [
                'show_cg_label', 'popup_show', 'popup_text', 
                'popup_extra_style'
            ]
        }),
    )
    tabs = [
        ('Overview', tab_overview),
        ('Env', tab_env),
        ('Extra UI', tab_extra_ui),
        ('3D Models', (Model3DTabularInline,)),
        ('2D Models', (Model2DTabularInline,)),
    ]
    
    def subscription_status_display(self, obj):
        return '{0}'.format(obj.subscription.status if obj.subscription else 'unpaid')
    subscription_status_display.short_description = 'Subscription status'
    
    def subscription_admin_link(self, obj):
        if obj.subscription_id:
            return '<a href="{0}" style="color: blue;" target="_blank">Edit subscription</a>'.format(
                reverse('admin:pinax_stripe_subscription_change', args=(obj.subscription_id,))
            )
        return '<span style="color: red;">Subscription does not exist</span>'
    subscription_admin_link.allow_tags = True
    subscription_admin_link.short_description = 'Subscription'

class TextureTabularInline(admin.TabularInline):
    model = Texture
    readonly_fields = ['file_preview']
    extra = 0
    
    def file_preview(self, obj):
        if obj.file and obj.file.url:
            return '<img src="{0}" style="width: 100px;">'.format(obj.file.url)
        return '<span style="color: red;">file does not exist</span>'
    file_preview.allow_tags = True
    file_preview.short_description = 'preview'

class AnimationTabularInline(admin.StackedInline):
    model = Animation
    extra = 0
    exclude = ['thumbnail_tmp']

class AnimationModelAdmin(admin.ModelAdmin):
    exclude = ['model3d']
    inlines = [AnimationTabularInline]
    
class AnimationModelTabularInline(admin.TabularInline):
    model = AnimationModel
    readonly_fields = ['type', 'animation_json', 'animation_model_admin_link']
    extra = 0
    
    def animation_json(self, obj):
        return '<input type="file" name="animation_json"/>'
    animation_json.allow_tags = True
    animation_json.short_description = 'reupload animation json'
    
    def animation_model_admin_link(self, obj):
        if obj.id:
            return '<a href="{0}" style="color: blue;" target="_blank">Edit animations</a>'.format(
                reverse('admin:projects_animationmodel_change', args=(obj.id,))
            )
        return '<span style="color: red;">3d model does not exist</span>'
    animation_model_admin_link.allow_tags = True
    animation_model_admin_link.short_description = '3d model'

class Model3DAdmin(TabbedModelAdmin):
    tab_overview = (
        (None, {
            'fields': [
                'file', 'thumbnail', 'camera_pos_x', 'camera_pos_y', 'camera_pos_z', 'rotate_camera', 
                'camera_min_distance', 'camera_max_distance',
            ]
        }),
    )
    tabs = [
        ('Overview', tab_overview),
        ('Textures', (TextureTabularInline, )),
        ('Animations', (AnimationModelTabularInline, )),
    ]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from . import utils
        animation_model_json = request.FILES.get('animation_json', None)
        if animation_model_json:
            animation_model_json = utils.get_animation_model([animation_model_json])
            utils.save_animation_json(obj, animation_model_json)

class TextureAdmin(admin.ModelAdmin):
    pass

class SkyboxAdmin(admin.ModelAdmin):
    pass

class MaterialAdmin(admin.ModelAdmin):
    pass

class LensFlareAdmin(admin.ModelAdmin):
    pass

class CalloutStyleAdmin(admin.ModelAdmin):
    pass

class LineStyleAdmin(admin.ModelAdmin):
    pass

class AnchorStyleAdmin(admin.ModelAdmin):
    pass

class CalloutAdmin(admin.ModelAdmin):
    pass

class GroundplaneAdmin(admin.ModelAdmin):
    pass

class ModelLensFlareAdmin(admin.ModelAdmin):
    pass

class ModelMaterialAdmin(admin.ModelAdmin):
    pass

class AnimationAdmin(admin.ModelAdmin):
    pass

class Model3DGalleryAdmin(admin.ModelAdmin):
    pass

class LightAdmin(admin.ModelAdmin):
    readonly_fields = ('source_prettified', 'source_usage_prettified')

    def source_prettified(self, instance):
        response = json.dumps(instance.source, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)
    
    def source_usage_prettified(self, instance):
        from .models import LIGHT_MODEL_USAGE
        response = json.dumps(LIGHT_MODEL_USAGE, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)

admin.site.register(Model3DGallery, Model3DGalleryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Light, LightAdmin)
admin.site.register(Model3D, Model3DAdmin)
admin.site.register(Texture, TextureAdmin)
admin.site.register(Skybox, SkyboxAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(LensFlare, LensFlareAdmin)
admin.site.register(CalloutStyle, CalloutStyleAdmin)
admin.site.register(LineStyle, LineStyleAdmin)
admin.site.register(AnchorStyle, AnchorStyleAdmin)
admin.site.register(Callout, CalloutAdmin)
admin.site.register(Groundplane, GroundplaneAdmin)
admin.site.register(ModelLensFlare,ModelLensFlareAdmin)
admin.site.register(ModelMaterial, ModelMaterialAdmin)
admin.site.register(Animation, AnimationAdmin)
admin.site.register(AnimationModel, AnimationModelAdmin)