# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-07 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postitem',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='PRICE_LABEL'),
        ),
    ]