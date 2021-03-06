# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-30 06:24
from __future__ import unicode_literals

import app.models.donation
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.localtime)),
                ('documented_at', models.CharField(blank=True,
                                                   max_length=10, verbose_name='Date Created in Y-M-D')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('tax_receipt_no', models.CharField(default=app.models.donation.gen_tax_receipt_no,
                                                    max_length=9, primary_key=True, serialize=False, verbose_name='Donation Number')),
                ('tax_receipt_created_at', models.DateTimeField(
                    blank=True, default=None, null=True)),
                ('pledge_date', models.DateField(
                    blank=True, null=True, verbose_name='Pledge Date')),
                ('donate_date', models.DateField(verbose_name='Receiving Date')),
                ('pick_up', models.CharField(blank=True,
                                             max_length=30, verbose_name='Pick Up Postal Code')),
            ],
            options={
                'permissions': (('generate_tax_receipt', 'Can generate tax receipts'),),
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.localtime)),
                ('documented_at', models.CharField(blank=True,
                                                   max_length=10, verbose_name='Date Created in Y-M-D')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('donor_name', models.CharField(
                    max_length=255, verbose_name='Donor Name')),
                ('contact_name', models.CharField(blank=True,
                                                  max_length=255, verbose_name='Contact Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('want_receipt', models.BooleanField(
                    verbose_name='Want Tax Receipt?')),
                ('telephone_number', models.CharField(
                    blank=True, max_length=255, verbose_name='Telephone #')),
                ('mobile_number', models.CharField(
                    blank=True, max_length=255, verbose_name='Mobile #')),
                ('address_line_one', models.CharField(blank=True,
                                                      max_length=255, verbose_name='Address Line 1')),
                ('address_line_two', models.CharField(blank=True,
                                                      max_length=255, verbose_name='Address Line 2')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
                ('province', models.CharField(choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('PE', 'Prince Edward Island'), (
                    'NS', 'Nova Scotia'), ('NL', 'Newfoundland and Labrador'), ('NB', 'New Brunswick'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut'), ('YT', 'Yukon')], max_length=255, verbose_name='Province')),
                ('postal_code', models.CharField(
                    max_length=10, verbose_name='Postal Code')),
                ('customer_ref', models.CharField(blank=True,
                                                  max_length=255, verbose_name='Customer Ref.')),
                ('source', models.CharField(blank=True,
                                            max_length=255, verbose_name='Source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.localtime)),
                ('documented_at', models.CharField(blank=True,
                                                   max_length=10, verbose_name='Date Created in Y-M-D')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('serial_number', models.CharField(blank=True,
                                                   max_length=255, verbose_name='Serial Number')),
                ('asset_tag', models.CharField(blank=True,
                                               max_length=255, verbose_name='Asset Tag')),
                ('particulars', models.CharField(blank=True,
                                                 max_length=255, verbose_name='Particulars')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('working', models.BooleanField(
                    max_length=255, verbose_name='Is Working?')),
                ('condition', models.CharField(blank=True,
                                               max_length=255, verbose_name='Condition')),
                ('quality', models.CharField(blank=True, choices=[
                 ('H', 'High'), ('M', 'Medium'), ('L', 'Low')], max_length=255, verbose_name='Quality')),
                ('batch', models.CharField(blank=True,
                                           max_length=255, verbose_name='Batch')),
                ('value', models.DecimalField(blank=True, decimal_places=2,
                                              default=0, max_digits=10, verbose_name='Value per Item')),
                ('verified', models.BooleanField(
                    default=False, verbose_name='Verified?')),
                ('status', models.CharField(blank=True, default='received',
                                            max_length=255, verbose_name='Status')),
                ('weight', models.CharField(blank=True,
                                            max_length=255, null=True, verbose_name='Weight')),
                ('valuation_date', models.DateField(
                    blank=True, null=True, verbose_name='Valuation Date')),
                ('valuation_supporting_doc', models.TextField(
                    blank=True, null=True, verbose_name='Valuation Support Doc')),
                ('notes', models.TextField(
                    blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'permissions': (('update_status', 'Can update item status'),),
            },
        ),
        migrations.CreateModel(
            name='ItemDevice',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('make', models.CharField(blank=True,
                                          max_length=255, verbose_name='Make')),
                ('model', models.CharField(blank=True,
                                           max_length=255, verbose_name='Model')),
                ('cpu_type', models.CharField(blank=True,
                                              max_length=255, null=True, verbose_name='CPU Type')),
                ('speed', models.CharField(blank=True,
                                           max_length=255, null=True, verbose_name='Speed')),
                ('memory', models.DecimalField(blank=True, decimal_places=2,
                                               max_digits=10, null=True, verbose_name='Memory (MB)')),
                ('hd_size', models.DecimalField(blank=True, decimal_places=2,
                                                max_digits=10, null=True, verbose_name='HD Size (GB)')),
                ('screen_size', models.CharField(blank=True,
                                                 max_length=255, null=True, verbose_name='Screen Size')),
                ('hdd_serial_number', models.CharField(blank=True,
                                                       max_length=255, null=True, verbose_name='HDD Serial Number')),
                ('operating_system', models.CharField(blank=True,
                                                      max_length=255, null=True, verbose_name='Operating System')),
            ],
        ),
        migrations.CreateModel(
            name='ItemDeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device_type', models.CharField(
                    max_length=255, verbose_name='Device Type')),
                ('category', models.CharField(choices=[('BATTERY', 'battery'), ('STORAGE', 'storage'), ('PERIPHERAL', 'peripheral'), ('POWER_SUPPLY', 'power supply'), ('COMPUTER', 'computer'), ('VIDEO', 'video'), ('CABLE', 'cable'), ('NETWORK', 'network'), ('TABLET', 'tablet'), ('DISPOSE', 'dispose'), ('SMALL_ELECTRIC_NON_IT', 'small electric non-IT'), (
                    'CAMERA', 'camera'), ('RECYLE', 'recyle'), ('PRINTER', 'printer'), ('ASSORTED', 'assorted'), ('COMPONENT', 'component'), ('PHONE', 'phone'), ('CASH', 'cash'), ('MONITOR', 'monitor'), ('AUDIO', 'audio'), ('SOFTWARE', 'software'), ('MISCELLANEOUS', 'miscellaneous')], max_length=255, verbose_name='Category')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='itemdevicetype',
            unique_together=set([('device_type', 'category')]),
        ),
        migrations.AddField(
            model_name='itemdevice',
            name='dtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='app.ItemDeviceType', verbose_name='Device Type'),
        ),
        migrations.AddField(
            model_name='item',
            name='device',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='app.ItemDevice'),
        ),
        migrations.AddField(
            model_name='item',
            name='donation',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='app.Donation'),
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='app.Donor'),
        ),
    ]
