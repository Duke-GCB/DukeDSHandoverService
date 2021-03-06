# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-30 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0005_auto_20170327_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='user_message',
            field=models.TextField(blank=True, help_text='Custom message to include about this item when sending notifications', null=True),
        ),
        migrations.AlterField(
            model_name='historicaldelivery',
            name='user_message',
            field=models.TextField(blank=True, help_text='Custom message to include about this item when sending notifications', null=True),
        ),
        migrations.AlterField(
            model_name='historicalshare',
            name='user_message',
            field=models.TextField(blank=True, help_text='Custom message to include about this item when sending notifications', null=True),
        ),
        migrations.AlterField(
            model_name='share',
            name='user_message',
            field=models.TextField(blank=True, help_text='Custom message to include about this item when sending notifications', null=True),
        ),
    ]
