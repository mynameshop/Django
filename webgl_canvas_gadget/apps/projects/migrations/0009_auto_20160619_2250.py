# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-19 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20160619_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='environment_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.EnvironmentImage'),
        ),
    ]