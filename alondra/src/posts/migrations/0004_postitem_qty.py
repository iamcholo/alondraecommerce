# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-07 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_postitem_taxes'),
    ]

    operations = [
        migrations.AddField(
            model_name='postitem',
            name='qty',
            field=models.IntegerField(default=0, verbose_name='QTY_LABEL'),
        ),
    ]
