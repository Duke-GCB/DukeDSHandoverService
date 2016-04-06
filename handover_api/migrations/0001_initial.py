# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=36)),
                ('from_user_id', models.CharField(max_length=36)),
                ('to_user_id', models.CharField(max_length=36)),
                ('state', models.IntegerField(choices=[(0, 'Initiated'), (1, 'Notified'), (4, 'Failed')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Handover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=36)),
                ('from_user_id', models.CharField(max_length=36)),
                ('to_user_id', models.CharField(max_length=36)),
                ('state', models.IntegerField(choices=[(0, 'Initiated'), (1, 'Notified'), (2, 'Accepted'), (3, 'Rejected')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dds_id', models.CharField(max_length=36, unique=True)),
                ('api_key', models.CharField(max_length=36)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='handover',
            unique_together=set([('project_id', 'from_user_id', 'to_user_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='draft',
            unique_together=set([('project_id', 'from_user_id', 'to_user_id')]),
        ),
    ]