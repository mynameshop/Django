# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-30 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20160630_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ground_plane',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Groundplane'),
        ),
    ]