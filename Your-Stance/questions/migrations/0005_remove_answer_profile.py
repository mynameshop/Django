# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-18 17:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_answer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='profile',
        ),
    ]