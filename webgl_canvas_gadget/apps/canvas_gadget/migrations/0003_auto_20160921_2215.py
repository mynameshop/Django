# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canvas_gadget', '0002_auto_20160917_2341'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'site settings', 'verbose_name_plural': 'site settings'},
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='homepage_text_how_it_work',
            field=models.CharField(default='Loren Iplus, Loren Implus, Loren Iplus, Loren Implus', max_length=512),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='homepage_text_step_1',
            field=models.CharField(default='Tell Us About Your Product', max_length=64),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='homepage_text_step_2',
            field=models.CharField(default='Let us do all the work', max_length=64),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='homepage_text_step_3',
            field=models.CharField(default='Publish the result with one line of code', max_length=64),
        ),
    ]