# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-23 10:25
from __future__ import unicode_literals

import apps.canvas_gadget.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('user_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('project_name', models.CharField(max_length=128)),
                ('project_description', models.CharField(max_length=512)),
                ('subscription_template', models.IntegerField(choices=[('1', 'silver'), ('2', 'gold'), ('3', 'platinum')], default=1)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectRequestImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('image', models.ImageField(upload_to=apps.canvas_gadget.models.get_project_request_folder)),
                ('project_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_gadget.ProjectRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]