# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from utilities.image_base64 import encode_image_2
from utilities.models import BaseDateTime
from django_countries.fields import CountryField
from posts.models import PostItem

# Create your models here.
STATUS_TYPES_CHOICES = (
    ('approved', 'Approved'),
    ('pending', 'Pending'),
    ('refunded', 'Refunded'),
    ('shipped', 'Approved'),
)

SHIPPING_TYPES_CHOICES = (
    ('shipped', 'Shipped'),
    ('in_transit', 'In_transit'),
)

CARRIER_TYPES_CHOICES = (
    ('USPS', 'USPS'),
    ('FEDEX', 'FEDEX'),
    ('DHL', 'DHL'),
    ('MRW', 'MRW'),
    ('ZOOM', 'ZOOM'),
)



class Orders(BaseDateTime):

    status = models.CharField(
            max_length=20,
            choices=STATUS_TYPES_CHOICES,
            default="approved"
        )
    
    autor = models.ForeignKey(
            User,
            verbose_name=_('AUTOR_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='orders_related_autor'
        )

    products = models.ManyToManyField(
            PostItem,
            verbose_name=_('MEDIA_ALBUM_TITLE_PLURAL'),
            related_name='orders_related_products',
            blank=True
        )

    total = models.FloatField(
            _('PERCENTAJE_LABEL'),
            max_length=255,
            blank=True      
        )
    def __unicode__(self):
        return self.status


    class Meta:
        verbose_name = _('DISCOUNTS_TITLE')
        verbose_name_plural = _('DISCOUNTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'orders'
        app_label = 'orders'


class Shipping(BaseDateTime):


    
    order = models.ForeignKey(
            Orders,
            verbose_name=_('AUTOR_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='orders_shipping_related_order'
        )

    
    product = models.ForeignKey(
            PostItem,
            verbose_name=_('AUTOR_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='orders_shipping_related_product'
        )
    status = models.CharField(
            max_length=20,
            choices=SHIPPING_TYPES_CHOICES,
            default="approved"
        )
    carrier = models.CharField(
            max_length=20,
            choices=CARRIER_TYPES_CHOICES,
            default="USPS"
        )
    
    tracking_number = models.TextField(
          
            blank=True,
        )

    def __unicode__(self):
        return self.status


    class Meta:
        verbose_name = _('SHIPPING_TITLE')
        verbose_name_plural = _('SHIPPING_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'orders'
        app_label = 'orders_shipping'
