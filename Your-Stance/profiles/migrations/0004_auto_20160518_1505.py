# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-18 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20160518_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxy',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='proxy',
            name='profile',
        ),
        migrations.DeleteModel(
            name='Proxy',
        ),
    ]