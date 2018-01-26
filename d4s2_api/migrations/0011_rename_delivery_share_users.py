# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-01-23 18:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0010_rename_delivery_dds_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryshareuser',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_users', to='d4s2_api.Delivery'),
        ),
    ]
