# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-12 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='currency',
            field=models.CharField(blank=True, choices=[(b'USD', 'USD'), (b'JPY', 'JPY'), (b'GBP', 'GBP'), (b'CAD', 'CAD'), (b'VEF', 'VEF')], max_length=3, verbose_name='CURRENCY_LABEL'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='email',
            field=models.CharField(blank=True, max_length=255, verbose_name='EMAIL_LABEL'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='payment_method',
            field=models.CharField(blank=True, choices=[(b'paypal', 'Paypal'), (b'mercadopago', 'Mercadopago'), (b'stripe', 'Stripe'), (b'bank_transfer', 'Bank transfer')], max_length=255, verbose_name='PERCENTAJE_LABEL'),
        ),
    ]