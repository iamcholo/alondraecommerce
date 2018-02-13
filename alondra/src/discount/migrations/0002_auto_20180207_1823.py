# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-07 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discounts',
            name='title',
        ),
        migrations.AlterField(
            model_name='discounts',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_item_product', to='posts.PostItem', verbose_name='AUTOR_LABEL'),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='start_date',
            field=models.DateTimeField(verbose_name='STAR_DATE_LABEL'),
        ),
    ]