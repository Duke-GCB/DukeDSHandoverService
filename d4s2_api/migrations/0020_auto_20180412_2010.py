# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-04-12 20:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0019_auto_20180412_1907'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='s3user',
            unique_together=set([('endpoint', 'user')]),
        ),
    ]
