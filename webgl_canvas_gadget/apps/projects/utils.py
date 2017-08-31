from __future__ import unicode_literals
import json
import re
from django.db import transaction
from .models import ANIMATION_TYPE_CHOICES, AnimationModel, Animation

def get_accepted_3d_file(files):
    file = None
    for f in files:
        if f.name == 'model.babylon':
            file = f
            break
    return file

def get_images(files):
    res = []
    for f in files:
        if f.content_type.startswith('image/'):
            res.append(f)
    return res

def get_animation_model(files):
    res = None
    for f in files:
        if f.name == 'animation.json':
            data = f.read().decode("utf-8").replace("\n","").replace("\t","")
            data = re.sub(",[ \t\r\n]+}", "}", data)
            data = re.sub(",[ \t\r\n]+\]", "]", data)
            res = json.loads(data)
    return res

@transaction.atomic
def save_animation_json(model3d, animation_model_json):
    animation_type_choices = dict(ANIMATION_TYPE_CHOICES)
    animation_type_choices = dict(zip(animation_type_choices.values(),animation_type_choices.keys()))
    
    animation_model, created = AnimationModel.objects.get_or_create(model3d = model3d)
    animation_model.type = animation_type_choices.get(animation_model_json['type'])
    animation_model.save()
    
    if not created:
        animation_model.animation_set.all().delete()
    
    for t_animation in animation_model_json['animations']:
        t_animation['animation_model'] = animation_model
        animation = Animation(
            **t_animation
        )
        animation.save()