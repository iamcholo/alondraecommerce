# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-07 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaimage',
            name='image',
            field=models.TextField(blank=True, verbose_name='IMAGE_LABEL'),
        ),
    ]
