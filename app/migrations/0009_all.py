# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-10 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20190814_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='All',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_import_historical', 'Can import historical data'), ('can_export_data', 'Can export data')),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
