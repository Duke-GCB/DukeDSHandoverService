# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-01-24 20:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0011_rename_delivery_share_users'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DukeDSProject',
        ),
        migrations.RemoveField(
            model_name='dukedsuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='dukedsuser',
            name='full_name',
        ),
    ]
