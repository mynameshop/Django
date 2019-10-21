# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-08 09:17
from __future__ import unicode_literals

import apps.projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_texture'),
    ]

    operations = [
        migrations.AddField(
            model_name='texture',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=apps.projects.models.upload_texture_to_media),
            preserve_default=False,
        ),
    ]