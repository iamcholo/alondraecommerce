# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
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
            related_name='discount_item_product'
        )

    percent = models.FloatField(
            _('PERCENTAJE_LABEL'),
            max_length=255,
            blank=True      
        )
    start_date = models.DateTimeField(
        _('STAR_DATE_LABEL'),
       
         
        )

    end_date = models.DateTimeField(
            _('END_DATE_LABEL'),
            blank=True
        )
    def __unicode__(self):
        return str(self.percent)


    class Meta:
        verbose_name = _('DISCOUNTS_TITLE')
        verbose_name_plural = _('DISCOUNTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'product_discounts'
        app_label = 'discount'
