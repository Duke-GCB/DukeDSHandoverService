# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handover_api', '0002_auto_20160329_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draft',
            name='state',
            field=models.IntegerField(choices=[(0, 'Initiated'), (1, 'Notified'), (4, 'Failed')], default=0),
        ),
    ]
