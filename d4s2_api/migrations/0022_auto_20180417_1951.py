# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-04-17 19:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0021_auto_20180416_1932'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='s3bucket',
            unique_together=set([('endpoint', 'name')]),
        ),
    ]
