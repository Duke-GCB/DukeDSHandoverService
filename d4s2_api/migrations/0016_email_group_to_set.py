# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-03-23 18:04
from __future__ import unicode_literals
from django.db import migrations


def copy_email_template_group_to_sets(apps, schema_editor):
    """
    For each EmailTemplate's group create a EmailTemplateSet and assign it to the EmailTemplate.
    """
    EmailTemplate = apps.get_model('d4s2_api', 'EmailTemplate')
    EmailTemplateSet = apps.get_model('d4s2_api', 'EmailTemplateSet')
    UserEmailTemplateSet = apps.get_model('d4s2_api', 'UserEmailTemplateSet')
    User = apps.get_model('auth', 'User')

    for email_template in EmailTemplate.objects.all():
        group_name = email_template.group.name
        email_template_set, _ = EmailTemplateSet.objects.get_or_create(name=group_name)
        email_template.template_set = email_template_set
        email_template.save()
        for user in User.objects.filter(groups__name=group_name):
            UserEmailTemplateSet.objects.get_or_create(user=user, email_template_set=email_template_set)


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0015_auto_20180323_1757'),
    ]

    operations = [
        migrations.RunPython(copy_email_template_group_to_sets, reverse_code=migrations.RunPython.noop),
    ]
