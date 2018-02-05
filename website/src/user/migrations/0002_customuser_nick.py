# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nick',
            field=models.CharField(unique=True, max_length=255, verbose_name='NICK_LABEL', blank=True),
        ),
    ]
