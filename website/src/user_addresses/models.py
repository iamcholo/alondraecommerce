# -*- coding: utf-8 -*-
from django.db import models
from user.models import CustomUser as User
from django.utils.translation import ugettext_lazy as _
from utilities.models import BaseDateTime
from django_countries.fields import CountryField


# Create your models here.
ADDRESSES_TYPES_CHOICES = (
    ('shipping', _('SHIPPING_ADDRESS_LABEL')),
    ('billing', _('BILLING_ADDRESS_LABEL')),
)

class Addresess(BaseDateTime):
    autor = models.ForeignKey(
            User,
            verbose_name=_('AUTOR_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='user_addresses_related_autor'
        )

    city = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            blank=True      
        )
    country = CountryField( null=True, blank=True)
    zip_code = models.CharField(
            _('ZIPCODE_LABEL'),
            max_length=255,
            blank=True      
        )
    first_name = models.CharField(
            _('FIRST_NAME_LABEL'),
            max_length=255,
            blank=True      
        )
    last_name = models.CharField(
            _('LAST_NAME_LABEL'),
            max_length=255,
            blank=True      
        )
    address_line_1 = models.CharField(
            _('ADDRESS_LINE_1_LABEL'),
            max_length=255,
            blank=True      
        )
    address_line_2 = models.CharField(
            _('ADDRESS_LINE_2_LABEL'),
            max_length=255,
            blank=True      
        ) 
    address_type = models.CharField(
            _('ADDRESS_LINE_2_LABEL'),
            max_length=25,
            choices=ADDRESSES_TYPES_CHOICES,
            blank=True,
            default="shipping"
        ) 
    
    def __unicode__(self):
        return self.city


    class Meta:
        verbose_name = _('DISCOUNTS_TITLE')
        verbose_name_plural = _('DISCOUNTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'user_addresses'
        app_label = 'user_addresses'
