# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-18 21:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_auth', '0004_auto_20161118_2047'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='oauthtoken',
            unique_together=set([('user', 'service'), ('service', 'token_json')]),
        ),
    ]