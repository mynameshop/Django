# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-27 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_model3d_rotate_camera'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slim_scroll_color',
            field=models.CharField(default='#ffffff', help_text='HEX color, as #RRGGBB or #RRGGBBOO', max_length=9),
        ),
    ]