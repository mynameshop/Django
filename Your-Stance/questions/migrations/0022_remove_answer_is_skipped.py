# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-29 12:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_auto_20160629_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='is_skipped',
        ),
    ]