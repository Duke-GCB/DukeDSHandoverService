# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-09-07 18:54
from __future__ import unicode_literals

from django.db import migrations

DELIVERY_CANCELED_TYPE = 'delivery_canceled'


def load_email_template_types(apps, schema_editor):
    EmailTemplateType = apps.get_model("d4s2_api", "EmailTemplateType")
    EmailTemplateType.objects.create(name=DELIVERY_CANCELED_TYPE)


def unload_email_template_types(apps, schema_editor):
    EmailTemplateType = apps.get_model("d4s2_api", "EmailTemplateType")
    for email_template_type in EmailTemplateType.objects.filter(name=DELIVERY_CANCELED_TYPE):
        email_template_type.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0031_auto_20180911_1500'),
    ]

    operations = [
        migrations.RunPython(load_email_template_types, reverse_code=unload_email_template_types),
    ]