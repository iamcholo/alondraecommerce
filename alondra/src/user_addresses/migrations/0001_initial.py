# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-11 20:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='CREATED_LABEL')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='MODIFIED_LABEL')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='TITLE_LABEL')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=255, verbose_name='ZIPCODE_LABEL')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='FIRST_NAME_LABEL')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='LAST_NAME_LABEL')),
                ('address_line_1', models.CharField(blank=True, max_length=255, verbose_name='ADDRESS_LINE_1_LABEL')),
                ('address_line_2', models.CharField(blank=True, max_length=255, verbose_name='ADDRESS_LINE_2_LABEL')),
                ('address_type', models.CharField(blank=True, choices=[(b'shipping', 'SHIPPING_ADDRESS_LABEL'), (b'billing', 'BILLING_ADDRESS_LABEL')], default=b'shipping', max_length=25, verbose_name='ADDRESS_LINE_2_LABEL')),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_addresses_related_autor', to=settings.AUTH_USER_MODEL, verbose_name='AUTOR_LABEL')),
            ],
            options={
                'get_latest_by': 'created',
                'ordering': ('-id',),
                'verbose_name_plural': 'DISCOUNTS_TITLE_PLURAL',
                'db_table': 'user_addresses',
                'verbose_name': 'DISCOUNTS_TITLE',
            },
        ),
    ]
