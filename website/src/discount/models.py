# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from utilities.image_base64 import encode_image_2
from utilities.models import BaseDateTime
from posts.models import PostItem
# Create your models here.

class Discounts(BaseDateTime):
    product = models.ForeignKey(
            PostItem,
            verbose_name=_('AUTOR_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='post_item_autor'
        )
    title = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            blank=True      
        )
    percent = models.FloatField(
            _('PERCENTAJE_LABEL'),
            max_length=255,
            blank=True      
        )
    start_date = models.DateTimeField(
        _('STAR_DATE_LABEL'),
       
         blank=True      
        )

    end_date = models.DateTimeField(
            _('END_DATE_LABEL'),
            blank=True
        )
    def __unicode__(self):
        return self.title


    class Meta:
        verbose_name = _('DISCOUNTS_TITLE')
        verbose_name_plural = _('DISCOUNTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'product_discounts'
        app_label = 'discount'
