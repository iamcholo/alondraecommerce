# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from utilities.models import BaseDateTime
from django_countries.fields import CountryField

# Create your models here.
PAYMENT_METHOD_TYPES_CHOICES = (
    ('paypal', _('Paypal')),
    ('mercadopago', _('Mercadopago')),
    ('stripe', _('Stripe')),
    ('bank_transfer', _('Bank transfer')),
)


CURRENCY_TYPES_CHOICES = (
    ('USD', _('USD')),
    ('JPY', _('JPY')),
    ('GBP', _('GBP')),
    ('CAD', _('CAD')),
    ('VEF', _('VEF')),
)

class PaymentMethod(BaseDateTime):
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
    city = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            blank=True      
        )
    country = CountryField( null=True, blank=True)
    amount = models.FloatField(
            _('PERCENTAJE_LABEL'),
            max_length=255,
            blank=True      
        )
    currency = models.FloatField(
            _('CURRENCY_LABEL'),
            max_length=3,
            blank=True,
            choices=CURRENCY_TYPES_CHOICES,
        )
    email = models.FloatField(
            _('EMAIL_LABEL'),
            max_length=255,
            blank=True      
        )
    payment_method = models.FloatField(
            _('PERCENTAJE_LABEL'),
            max_length=255,
            blank=True,
            choices=PAYMENT_METHOD_TYPES_CHOICES,
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
