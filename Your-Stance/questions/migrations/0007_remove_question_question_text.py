# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 13:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20160518_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
    ]