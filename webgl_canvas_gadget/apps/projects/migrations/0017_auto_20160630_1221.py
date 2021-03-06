# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-30 06:21
from __future__ import unicode_literals

import apps.projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20160629_1721'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EnvironmentImage',
            new_name='Skybox',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='environment_image',
            new_name='skybox',
        ),
        migrations.AlterField(
            model_name='project',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=apps.projects.models.upload_project_thumbnail),
        ),
    ]
