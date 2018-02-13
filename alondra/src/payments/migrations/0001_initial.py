# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-12 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='CREATED_LABEL')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='MODIFIED_LABEL')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='FIRST_NAME_LABEL')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='LAST_NAME_LABEL')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='TITLE_LABEL')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('amount', models.FloatField(blank=True, max_length=255, verbose_name='PERCENTAJE_LABEL')),
                ('currency', models.FloatField(blank=True, choices=[(b'USD', 'USD'), (b'JPY', 'JPY'), (b'GBP', 'GBP'), (b'CAD', 'CAD'), (b'VEF', 'VEF')], max_length=3, verbose_name='CURRENCY_LABEL')),
                ('email', models.FloatField(blank=True, max_length=255, verbose_name='EMAIL_LABEL')),
                ('payment_method', models.FloatField(blank=True, choices=[(b'paypal', 'Paypal'), (b'mercadopago', 'Mercadopago'), (b'stripe', 'Stripe'), (b'bank_transfer', 'Bank transfer')], max_length=255, verbose_name='PERCENTAJE_LABEL')),
            ],
            options={
                'get_latest_by': 'created',
                'ordering': ('-id',),
                'verbose_name_plural': 'DISCOUNTS_TITLE_PLURAL',
                'db_table': 'payment_methods',
                'verbose_name': 'DISCOUNTS_TITLE',
            },
        ),
    ]