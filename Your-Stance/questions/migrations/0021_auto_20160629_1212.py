# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-29 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0020_skipanswer'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='skipanswer',
            unique_together=set([('user', 'question')]),
        ),
    ]