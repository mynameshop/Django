# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-16 15:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0039_auto_20160816_2147'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='modelmaterial',
            unique_together=set([('model3d', 'compNum', 'subCompNum')]),
        ),
    ]
