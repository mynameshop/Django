# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-18 17:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_remove_answer_profile'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('user', 'question')]),
        ),
    ]
