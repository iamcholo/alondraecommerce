# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from utilities.models import BaseDateTime
from utilities.models import BasePublish

class GlobalConfig(BaseDateTime, BasePublish):
    sitename = models.CharField(
            _('SITE_NAME_LABEL'),
            max_length=255,
            unique=True,
            blank=True      
        )
    sitelink = models.CharField(
            _('SITE_LINK_LABEL'),
            max_length=255,
            unique=True,
            blank=True      
        )
    meta_title = models.CharField(
            _('META_TITLE_LABEL'),
            max_length=255,
 
        )
    meta_description = models.TextField(
            _('META_DESCRIPTION_LABEL'),
            blank=True
        )
    def __unicode__(self):
        return self.sitename
    class Meta:
        verbose_name = _('GLOBAL_CONFIG_TITLE')
        verbose_name_plural = _('GLOBAL_CONFIG_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'global_config_config'
        app_label = 'global_config'
