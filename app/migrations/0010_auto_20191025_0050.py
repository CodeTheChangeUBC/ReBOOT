# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-25 04:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_all'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='all',
            options={'default_permissions': (), 'managed': False, 'permissions': (('can_import_historical', 'Can import historical data'), ('can_import_third_party', 'Can import third party data'), ('can_import_website', 'Can import website data'), ('can_export_data', 'Can export data'))},
        ),
    ]