# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-25 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0021_auto_20160721_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notification_like',
            field=models.BooleanField(default=True),
        ),
    ]
