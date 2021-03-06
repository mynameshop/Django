# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-24 09:52
from __future__ import unicode_literals

import apps.projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20160622_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='model3d',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='model3d',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='model3d',
            name='thumbnail_tmp',
            field=models.ImageField(blank=True, default='', null=True, upload_to=apps.projects.models.upload_model_to_media),
        ),
    ]
