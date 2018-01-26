# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-01-22 20:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d4s2_api', '0009_migrate_share_delivery_dds_fields'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='delivery',
            unique_together=set([('project_new', 'from_user_new', 'to_user_new')]),
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='project',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='share_to_users',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='to_user',
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='from_user_new',
            new_name='from_user_id',
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='project_new',
            new_name='project_id',
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='to_user_new',
            new_name='to_user_id',
        ),
        migrations.AlterUniqueTogether(
            name='delivery',
            unique_together=set([('project_id', 'from_user_id', 'to_user_id')]),
        ),
        migrations.RemoveField(
            model_name='historicaldelivery',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='historicaldelivery',
            name='project',
        ),
        migrations.RemoveField(
            model_name='historicaldelivery',
            name='to_user',
        ),
        migrations.RenameField(
            model_name='historicaldelivery',
            old_name='from_user_new',
            new_name='from_user_id',
        ),
        migrations.RenameField(
            model_name='historicaldelivery',
            old_name='project_new',
            new_name='project_id',
        ),
        migrations.RenameField(
            model_name='historicaldelivery',
            old_name='to_user_new',
            new_name='to_user_id',
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=set([('project_new', 'from_user_new', 'to_user_new', 'role')]),
        ),
        migrations.RemoveField(
            model_name='share',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='share',
            name='project',
        ),
        migrations.RemoveField(
            model_name='share',
            name='to_user',
        ),
        migrations.RenameField(
            model_name='share',
            old_name='from_user_new',
            new_name='from_user_id',
        ),
        migrations.RenameField(
            model_name='share',
            old_name='project_new',
            new_name='project_id',
        ),
        migrations.RenameField(
            model_name='share',
            old_name='to_user_new',
            new_name='to_user_id',
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=set([('project_id', 'from_user_id', 'to_user_id', 'role')]),
        ),
        migrations.RemoveField(
            model_name='historicalshare',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='historicalshare',
            name='project',
        ),
        migrations.RemoveField(
            model_name='historicalshare',
            name='to_user',
        ),
        migrations.RenameField(
            model_name='historicalshare',
            old_name='from_user_new',
            new_name='from_user_id',
        ),
        migrations.RenameField(
            model_name='historicalshare',
            old_name='project_new',
            new_name='project_id',
        ),
        migrations.RenameField(
            model_name='historicalshare',
            old_name='to_user_new',
            new_name='to_user_id',
        ),
        migrations.AlterField(
            model_name='deliveryshareuser',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_user_ids', to='d4s2_api.Delivery'),
        ),
        migrations.AlterUniqueTogether(
            name='deliveryshareuser',
            unique_together=set([('dds_id', 'delivery')]),
        ),
    ]
