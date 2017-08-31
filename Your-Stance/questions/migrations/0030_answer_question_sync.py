# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from questions.models import Answer


def copy_stancequestion_id(apps, schema_editor):
    answers = Answer.objects.all()
    for answer in answers:
        if answer.stance and answer.stance.question:
            answer.question = answer.stance.question
            answer.save()
            

def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0029_answer_question'),
    ]

    operations = [
        migrations.RunPython(copy_stancequestion_id, reverse_func),
    ]
