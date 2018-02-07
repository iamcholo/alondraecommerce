# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from utilities.image_base64 import encode_image_2
from utilities.models import BaseDateTime
from django_countries.fields import CountryField

# Create your models here.

class Taxes(BaseDateTime):

    city = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            blank=True      
        )
    country = CountryField( null=True, blank=True)
    percent = models.FloatField(
            _('PERCENTAJE_LABEL'),
            max_length=255,
            blank=True      
        )
    def __unicode__(self):
        return self.city


    class Meta:
        verbose_name = _('DISCOUNTS_TITLE')
        verbose_name_plural = _('DISCOUNTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'taxes'
        app_label = 'taxes'
