# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
from utilities.image_base64 import encode_image
from utilities.models import BaseDateTime
from utilities.models import BaseSeo
from utilities.models import BasePublish

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'item' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['item']))
            kwargs['object_id'] = kwargs['item'].pk
            del(kwargs['item'])
        return super(ItemManager, self).get(*args, **kwargs)

class GlobalyUrls(MPTTModel, BaseSeo, BaseDateTime):
    parent = TreeForeignKey(
            'self',
            verbose_name=_('PARENT_LABEL'),
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='globaly_urls_parent'
        )
    is_nav = models.BooleanField(
            _('IS_NAV_LABEL'),
            default=False,
        )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('CONTENT_TYPE_LABEL'),
        #limit_choices_to=limit,
        null=True,
        blank=True,
    )
    
    object_id = models.PositiveIntegerField(
        verbose_name=_('RELATED_OBJECT_LABEL'),
        null=True,
    )
    
    content_object = GenericForeignKey(
            'content_type', 
            'object_id'
        )
    
    view_name = models.TextField(
            _('VIEW_NAME_LABEL'),
            max_length=255,
            null=True,
            blank=True,
        )
    paginated = models.BooleanField(
            _('PAGINATED_LABEL'),
            default=False
        )
    objects = ItemManager()
    def __unicode__(self):
        return self.slug

    def get_item(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_item(self, item):
        self.content_type = ContentType.objects.get_for_model(type(item))
        self.object_id = item.pk

    item = property(get_item, set_item)

    class Meta:
        abstract = True
        verbose_name = _('GLOBALY_URLS_TITLE')
        verbose_name_plural = _('GLOBALY_URLS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'globaly_urls'
        app_label = 'globaly'

def slug_default(instance):
    object_type = ContentType.objects.get_for_model(instance)
    url = GlobalyUrls.objects.filter(
        content_type__pk=object_type.id,
        object_id=instance.id
    )
  
    url = next(iter(url), None)
    if url is not None:
        return url.slug
    return None

def get_meta(instance):
    object_type = ContentType.objects.get_for_model(instance)
    meta = GlobalyUrls.objects.filter(
        content_type__pk=object_type.id,
        object_id=instance.id
    )
    meta = next(iter(meta), None)
    
    if meta is not None:
        
        return meta.slug, meta.meta_title, meta.meta_description
    
    return None, None, None

class GlobalyTags(BasePublish,BaseDateTime, BaseSeo):

    name = models.CharField(
            _('NAME_LABEL'),
            max_length=255,
            unique=True,
            blank=True      
        )
    
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _('GLOBALY_TAG_TITLE')
        verbose_name_plural = _('GLOBALY_TAG_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'globaly_tags'
        app_label = 'globaly'

