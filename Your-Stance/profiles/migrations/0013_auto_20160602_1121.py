# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_profile_is_famous'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='headline',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
    ]
